import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';
import { environment } from '../../environments/environment';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;
  const routerStub = { navigate: jasmine.createSpy('navigate') };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [{ provide: Router, useValue: routerStub }],
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
    localStorage.clear();
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('login persiste token y usuario', () => {
    service.login('user@test.com', 'password12').subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    expect(req.request.method).toBe('POST');
    req.flush({ access_token: 'jwt-test', user: { id: 1, email: 'user@test.com' } });
    expect(service.token()).toBe('jwt-test');
    expect(service.user()?.email).toBe('user@test.com');
  });

  it('logout limpia sesión tras login', () => {
    service.login('u@test.com', 'password12').subscribe();
    httpMock
      .expectOne(`${environment.apiUrl}/auth/login`)
      .flush({ access_token: 'tok', user: { id: 1, email: 'u@test.com' } });
    expect(service.token()).toBe('tok');
    service.logout();
    expect(service.token()).toBeNull();
    expect(routerStub.navigate).toHaveBeenCalledWith(['/login']);
  });
});
