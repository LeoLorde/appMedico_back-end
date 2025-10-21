from flask import request, jsonify
from controllers.notification_controller import send_notification_to_user
from database import get_db

def confirm_appointment(appointment_id):
    """
    Médico confirma uma consulta
    PUT /api/appointments/<id>/confirm
    """
    try:
        doctor_id = request.user['id']  # Médico que está confirmando
        
        db = get_db()
        
        # 1. Buscar dados da consulta
        appointment = db.execute(
            'SELECT * FROM appointments WHERE id = %s',
            (appointment_id,)
        ).fetchone()
        
        if not appointment:
            return jsonify({'error': 'Consulta não encontrada'}), 404
        
        client_id = appointment['client_id']
        appointment_date = appointment['date']
        appointment_time = appointment['time']
        
        # 2. Atualizar status da consulta
        db.execute(
            'UPDATE appointments SET status = %s WHERE id = %s',
            ('confirmed', appointment_id)
        )
        db.commit()
        
        # 3. Buscar nome do médico
        doctor = db.execute(
            'SELECT name FROM doctors WHERE id = %s',
            (doctor_id,)
        ).fetchone()
        doctor_name = doctor['name']
        
        # 4. ENVIAR NOTIFICAÇÃO PARA O CLIENTE
        send_notification_to_user(
            user_id=client_id,
            user_type='client',
            title='Consulta Confirmada!',
            body=f'Dr(a). {doctor_name} confirmou sua consulta para {appointment_date} às {appointment_time}',
            notification_type='appointment_confirmed',
            data={
                'appointmentId': appointment_id,
                'doctorId': doctor_id,
                'date': str(appointment_date),
                'time': str(appointment_time)
            }
        )
        
        print(f'[v0] Notificação de confirmação enviada para cliente {client_id}')
        
        return jsonify({
            'message': 'Consulta confirmada com sucesso',
            'appointment': dict(appointment)
        }), 200
        
    except Exception as e:
        print(f'[v0] Erro ao confirmar consulta: {str(e)}')
        return jsonify({'error': 'Erro ao confirmar consulta'}), 500