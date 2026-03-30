import { AbstractControl, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';

/** Correo con formato razonable (más estricto que Validators.email por defecto). */
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

/** Obligatorio ignorando solo espacios al inicio/final. */
export function requiredTrimmed(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const raw = (control.value ?? '').toString().trim();
    return raw.length ? null : { requiredTrimmed: true };
  };
}

/** Teléfono: dígitos, espacios, +, guiones; longitud mínima 7. */
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

/** Select medicamento: exige un id numérico elegido. */
export function medicamentoSeleccionado(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const v = control.value;
    if (v === null || v === undefined || v === '') {
      return { required: true };
    }
    return null;
  };
}

/** Composición habitual para correo en formularios de auth. */
export const emailLoginValidators = [Validators.required, emailStrict()];
export const passwordLoginValidators = [Validators.required, Validators.minLength(8)];
