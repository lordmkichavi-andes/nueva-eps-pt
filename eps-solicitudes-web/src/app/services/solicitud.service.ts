import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Medicamento {
  id: number;
  nombre: string;
  es_pos: boolean;
}

export interface SolicitudItem {
  id: number;
  medicamento_id: number;
  medicamento_nombre: string;
  es_pos: boolean;
  numero_orden: string | null;
  direccion: string | null;
  telefono: string | null;
  correo: string | null;
  created_at: string;
}

export interface SolicitudesPage {
  items: SolicitudItem[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export interface CrearSolicitudPayload {
  medicamento_id: number;
  numero_orden?: string;
  direccion?: string;
  telefono?: string;
  correo?: string;
}

@Injectable({ providedIn: 'root' })
export class SolicitudService {
  constructor(private readonly http: HttpClient) {}

  listMedicamentos(): Observable<Medicamento[]> {
    return this.http.get<Medicamento[]>(`${environment.apiUrl}/api/medicamentos`);
  }

  crearSolicitud(body: CrearSolicitudPayload): Observable<unknown> {
    return this.http.post(`${environment.apiUrl}/api/solicitudes`, body);
  }

  listSolicitudes(page = 1, perPage = 10): Observable<SolicitudesPage> {
    const params = new HttpParams().set('page', String(page)).set('per_page', String(perPage));
    return this.http.get<SolicitudesPage>(`${environment.apiUrl}/api/solicitudes`, { params });
  }
}
