import { CommonModule } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import {
  emailStrict,
  medicamentoSeleccionado,
  requiredTrimmed,
  telefonoColombia,
} from '../../shared/form-validators';
import {
  CrearSolicitudPayload,
  Medicamento,
  SolicitudItem,
  SolicitudService,
} from '../../services/solicitud.service';

@Component({
  selector: 'app-solicitudes',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './solicitudes.component.html',
  styleUrl: './solicitudes.component.scss',
})
export class SolicitudesComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly solicitudService = inject(SolicitudService);
  readonly auth = inject(AuthService);

  medicamentos = signal<Medicamento[]>([]);
  lista = signal<SolicitudItem[]>([]);
  total = signal(0);
  page = signal(1);
  perPage = 10;
  pages = signal(0);
  loadingList = false;
  loadingForm = false;
  errorForm: string | null = null;
  errorList: string | null = null;
  successMsg: string | null = null;
  formSubmitted = false;

  form = this.fb.group({
    medicamento_id: [null as number | null, medicamentoSeleccionado()],
    numero_orden: [''],
    direccion: [''],
    telefono: [''],
    correo: [''],
  });

  private readonly selectedMedicamentoId = signal<number | null>(null);

  readonly medicamentoSeleccionado = computed(() => {
    const id = this.selectedMedicamentoId();
    if (id == null) return null;
    return this.medicamentos().find((m) => m.id === id) ?? null;
  });

  readonly esNoPos = computed(() => {
    const m = this.medicamentoSeleccionado();
    return m ? !m.es_pos : false;
  });

  ngOnInit(): void {
    this.loadMedicamentos();
    this.loadPage(1);
    this.selectedMedicamentoId.set(this.form.controls.medicamento_id.value);
    this.form.controls.medicamento_id.valueChanges.subscribe((v) => {
      this.selectedMedicamentoId.set(v);
      this.applyNoPosValidators();
    });
  }

  private applyNoPosValidators(): void {
    const m = this.medicamentoSeleccionado();
    const extra = ['numero_orden', 'direccion', 'telefono', 'correo'] as const;
    if (m && !m.es_pos) {
      this.form.controls.numero_orden.setValidators([requiredTrimmed()]);
      this.form.controls.direccion.setValidators([requiredTrimmed()]);
      this.form.controls.telefono.setValidators([requiredTrimmed(), telefonoColombia()]);
      this.form.controls.correo.setValidators([requiredTrimmed(), emailStrict()]);
    } else {
      extra.forEach((k) => this.form.controls[k].clearValidators());
    }
    extra.forEach((k) => this.form.controls[k].updateValueAndValidity({ emitEvent: false }));
  }

  loadMedicamentos(): void {
    this.solicitudService.listMedicamentos().subscribe({
      next: (items) => this.medicamentos.set(items),
      error: () => {
        this.errorForm = 'No se pudieron cargar los medicamentos';
      },
    });
  }

  loadPage(p: number): void {
    this.loadingList = true;
    this.errorList = null;
    this.solicitudService.listSolicitudes(p, this.perPage).subscribe({
      next: (res) => {
        this.lista.set(res.items);
        this.total.set(res.total);
        this.page.set(res.page);
        this.pages.set(res.pages);
        this.loadingList = false;
      },
      error: () => {
        this.loadingList = false;
        this.errorList = 'No se pudieron cargar las solicitudes';
      },
    });
  }

  showError(name: 'medicamento_id' | 'numero_orden' | 'direccion' | 'telefono' | 'correo'): boolean {
    const c = this.form.controls[name];
    return c.invalid && (c.touched || this.formSubmitted);
  }

  enviar(): void {
    this.formSubmitted = true;
    this.applyNoPosValidators();
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.errorForm = null;
    this.successMsg = null;
    this.loadingForm = true;
    const raw = this.form.getRawValue();
    const payload: CrearSolicitudPayload = {
      medicamento_id: raw.medicamento_id!,
    };
    const m = this.medicamentoSeleccionado();
    if (m && !m.es_pos) {
      payload.numero_orden = raw.numero_orden!.trim();
      payload.direccion = raw.direccion!.trim();
      payload.telefono = raw.telefono!.trim();
      payload.correo = raw.correo!.trim();
    }
    this.solicitudService.crearSolicitud(payload).subscribe({
      next: () => {
        this.loadingForm = false;
        this.successMsg = 'Solicitud creada correctamente';
        this.formSubmitted = false;
        this.form.reset({
          medicamento_id: null,
          numero_orden: '',
          direccion: '',
          telefono: '',
          correo: '',
        });
        this.selectedMedicamentoId.set(null);
        this.applyNoPosValidators();
        this.loadPage(this.page());
      },
      error: (err) => {
        this.loadingForm = false;
        this.errorForm = err?.error?.error ?? 'Error al crear la solicitud';
      },
    });
  }

  prev(): void {
    const p = this.page();
    if (p > 1) this.loadPage(p - 1);
  }

  next(): void {
    const p = this.page();
    if (p < this.pages()) this.loadPage(p + 1);
  }
}
