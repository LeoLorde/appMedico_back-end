from typing import Dict, Any, List, Optional
from classes.cpf import CPF
from classes.email import Email
from classes.crm import CRM
import uuid

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, errors: Dict[str, str]):
        self.errors = errors
        super().__init__(str(errors))

class InputValidator:
    """Centralized input validation utility"""
    
    @staticmethod
    def validate_client_data(data: Dict[str, Any], is_update: bool = False) -> Dict[str, Any]:
        """Validate client input data"""
        errors = {}
        validated = {}
        
        if 'username' in data:
            username = data.get('username', '').strip()
            if not username:
                errors['username'] = 'Username é obrigatório'
            elif len(username) < 3:
                errors['username'] = 'Username deve ter no mínimo 3 caracteres'
            elif len(username) > 50:
                errors['username'] = 'Username deve ter no máximo 50 caracteres'
            else:
                validated['username'] = username
        elif not is_update:
            errors['username'] = 'Username é obrigatório'
        
        if 'password' in data:
            password = data.get('password', '')
            if not password and not is_update:
                errors['password'] = 'Password é obrigatório'
            elif password and len(password) < 6:
                errors['password'] = 'Password deve ter no mínimo 6 caracteres'
            elif password:
                validated['password'] = password
        elif not is_update:
            errors['password'] = 'Password é obrigatório'
        
        if 'email' in data:
            email = data.get('email', '').strip()
            if email:
                if not Email.is_valid(email):
                    errors['email'] = 'Email inválido'
                else:
                    validated['email'] = Email.parse(email)
            elif not is_update:
                errors['email'] = 'Email é obrigatório'
        elif not is_update:
            errors['email'] = 'Email é obrigatório'
        
        if 'cpf' in data:
            cpf = data.get('cpf', '').strip()
            if cpf:
                if not CPF.validator(cpf):
                    errors['cpf'] = 'CPF inválido'
                else:
                    validated['cpf'] = CPF.parse_cpf(cpf)
            elif not is_update:
                errors['cpf'] = 'CPF é obrigatório'
        elif not is_update:
            errors['cpf'] = 'CPF é obrigatório'
    
        if errors:
            raise ValidationError(errors)
        
        return validated
    
    @staticmethod
    def validate_doctor_data(data: Dict[str, Any], is_update: bool = False) -> Dict[str, Any]:
        """Validate doctor input data"""
        errors = {}
        validated = {}
        
        if 'username' in data:
            username = data.get('username', '').strip()
            if not username:
                errors['username'] = 'Username é obrigatório'
            elif len(username) < 3:
                errors['username'] = 'Username deve ter no mínimo 3 caracteres'
            elif len(username) > 50:
                errors['username'] = 'Username deve ter no máximo 50 caracteres'
            else:
                validated['username'] = username
        elif not is_update:
            errors['username'] = 'Username é obrigatório'
        
        if 'password' in data:
            password = data.get('password', '')
            if not password and not is_update:
                errors['password'] = 'Password é obrigatório'
            elif password and len(password) < 6:
                errors['password'] = 'Password deve ter no mínimo 6 caracteres'
            elif password:
                validated['password'] = password
        elif not is_update:
            errors['password'] = 'Password é obrigatório'
        
        if 'email' in data:
            email = data.get('email', '').strip()
            if email:
                if not Email.is_valid(email):
                    errors['email'] = 'Email inválido'
                else:
                    validated['email'] = Email.parse(email)
            elif not is_update:
                errors['email'] = 'Email é obrigatório'
        elif not is_update:
            errors['email'] = 'Email é obrigatório'
        
        if 'crm' in data:
            crm = data.get('crm', '').strip()
            if crm:
                if not CRM.is_valid(crm):
                    errors['crm'] = 'CRM inválido'
                else:
                    validated['crm'] = CRM.parse(crm)
            elif not is_update:
                errors['crm'] = 'CRM é obrigatório'
        elif not is_update:
            errors['crm'] = 'CRM é obrigatório'
        
        if 'specialty' in data:
            specialty = data.get('specialty', '').strip()
            if specialty:
                if len(specialty) < 2:
                    errors['specialty'] = 'Especialidade deve ter no mínimo 2 caracteres'
                elif len(specialty) > 100:
                    errors['specialty'] = 'Especialidade deve ter no máximo 100 caracteres'
                else:
                    validated['specialty'] = specialty
        
        if errors:
            raise ValidationError(errors)
        
        return validated
    
    @staticmethod
    def validate_appointment_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate appointment input data"""
        errors = {}
        validated = {}
        
        if 'client_id' in data:
            client_id = data.get('client_id', '').strip()
            try:
                uuid.UUID(client_id)
                validated['client_id'] = client_id
            except ValueError:
                errors['client_id'] = 'Client ID inválido, deve ser um UUID válido'
        else:
            errors['client_id'] = 'Client ID é obrigatório'
        
        if 'doctor_id' in data:
            doctor_id = data.get('doctor_id', '').strip()
            try:
                uuid.UUID(doctor_id)
                validated['doctor_id'] = doctor_id
            except ValueError:
                errors['doctor_id'] = 'Doctor ID inválido, deve ser um UUID válido'
        else:
            errors['doctor_id'] = 'Doctor ID é obrigatório'
        
        if 'date' in data:
            date = data.get('date', '').strip()
            if not date:
                errors['date'] = 'Data é obrigatória'
            else:
                validated['date'] = date
        else:
            errors['date'] = 'Data é obrigatória'
        
        if 'time' in data:
            time = data.get('time', '').strip()
            if not time:
                errors['time'] = 'Horário é obrigatório'
            else:
                validated['time'] = time
        else:
            errors['time'] = 'Horário é obrigatório'
        
        if errors:
            raise ValidationError(errors)
        
        return validated

    @staticmethod
    def sanitize_output(data: Dict[str, Any], exclude_fields: List[str] = None) -> Dict[str, Any]:
        """Remove sensitive fields from output"""
        if exclude_fields is None:
            exclude_fields = ['password', 'password_hash']
        
        return {k: v for k, v in data.items() if k not in exclude_fields}
