import { AbstractControl, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';

export function emailStrict(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const raw = (control.value ?? '').toString().trim();
    if (!raw) {
      return null;
    }
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(raw);
    return ok ? null : { emailStrict: true };
  };
}

export function requiredTrimmed(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const raw = (control.value ?? '').toString().trim();
    return raw.length ? null : { requiredTrimmed: true };
  };
}

export function telefonoColombia(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const raw = (control.value ?? '').toString().trim();
    if (!raw) {
      return null;
    }
    const digits = raw.replace(/\D/g, '');
    if (digits.length < 7 || digits.length > 15) {
      return { telefono: true };
    }
    return null;
  };
}

export function medicamentoSeleccionado(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const v = control.value;
    if (v === null || v === undefined || v === '') {
      return { required: true };
    }
    return null;
  };
}

export const emailLoginValidators = [Validators.required, emailStrict()];
export const passwordLoginValidators = [Validators.required, Validators.minLength(8)];
