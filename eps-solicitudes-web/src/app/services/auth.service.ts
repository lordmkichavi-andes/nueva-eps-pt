import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface UserInfo {
  id: number;
  email: string;
}

export interface LoginResponse {
  access_token: string;
  user: UserInfo;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly tokenKey = 'eps_access_token';
  private readonly userKey = 'eps_user';

  readonly token = signal<string | null>(this.loadToken());
  readonly user = signal<UserInfo | null>(this.loadUser());

  constructor(
    private readonly http: HttpClient,
    private readonly router: Router,
  ) {}

  private loadToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  private loadUser(): UserInfo | null {
    const raw = localStorage.getItem(this.userKey);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as UserInfo;
    } catch {
      return null;
    }
  }

  isLoggedIn(): boolean {
    return !!this.token();
  }

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${environment.apiUrl}/auth/login`, { email, password })
      .pipe(tap((res) => this.persistSession(res.access_token, res.user)));
  }

  register(email: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${environment.apiUrl}/auth/register`, { email, password })
      .pipe(tap((res) => this.persistSession(res.access_token, res.user)));
  }

  private persistSession(accessToken: string, user: UserInfo): void {
    localStorage.setItem(this.tokenKey, accessToken);
    localStorage.setItem(this.userKey, JSON.stringify(user));
    this.token.set(accessToken);
    this.user.set(user);
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    this.token.set(null);
    this.user.set(null);
    void this.router.navigate(['/login']);
  }
}
