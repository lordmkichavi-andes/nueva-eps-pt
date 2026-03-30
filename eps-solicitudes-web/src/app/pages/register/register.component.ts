import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import {
  emailLoginValidators,
  passwordLoginValidators,
} from '../../shared/form-validators';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  error: string | null = null;
  loading = false;
  submitted = false;

  form = this.fb.nonNullable.group({
    email: ['', emailLoginValidators],
    password: ['', passwordLoginValidators],
  });

  submit(): void {
    this.submitted = true;
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.error = null;
    this.loading = true;
    const { email, password } = this.form.getRawValue();
    this.auth.register(email.trim(), password).subscribe({
      next: () => void this.router.navigate(['/solicitudes']),
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.error ?? 'No se pudo registrar';
      },
      complete: () => {
        this.loading = false;
      },
    });
  }

  showError(controlName: 'email' | 'password'): boolean {
    const c = this.form.controls[controlName];
    return c.invalid && (c.touched || this.submitted);
  }
}
