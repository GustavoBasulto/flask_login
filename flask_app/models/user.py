import os

from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utils.regex import EMAIL_REGEX


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password,  created_at, updated_at ) VALUES ( %(nombre)s , %(apellido)s , %(mail)s , %(contraseña)s, NOW() , NOW() );"
        return connectToMySQL(os.environ.get("BBDD_NAME")).query_db( query, data )

    @classmethod
    def email_bbdd(cls, mail ):
        query = "select * from users WHERE email = %(mail)s;"
        data={
            'mail':mail}
        results = connectToMySQL(os.environ.get("BBDD_NAME")).query_db( query, data )
        if not results:
            return False
        data_com = results [0]
        print(data_com)
        
        
        return data_com
    

    @classmethod
    def validate_user(cls, data):
        is_valid = True
        if len((data['nombre'])) < 2:
            flash("Debes ingresar minino 2 letras en el nombre.", "error")
            is_valid = False
        if len(data['apellido']) < 2:
            flash("Debes ingresar minino 2 letras en el apellido.", "error")
            is_valid = False
        if len(data['contraseña']) != 8:
            flash("Debes ingresar 8 caracteres en la contraseña.", "error")
            is_valid = False
        if data['contraseña'] != data['confirm_contraseña'] :
            flash("Las contraseñas deben ser iguales", "error")
            is_valid = False
        if not EMAIL_REGEX.match(data['mail']):
            flash("Formato de correo incorrecto", "error")
            is_valid = False
        
        return is_valid

        
    @classmethod
    def validate_login(cls, data):
        is_valid = True
        if len(data['contraseña']) <1 :
            flash("Debes ingresar la contraseña.", "error")
            is_valid = False
        if len(data['mail']) <1 :
            flash("Debes ingresar el correo.", "error")
            is_valid = False
        
        return is_valid