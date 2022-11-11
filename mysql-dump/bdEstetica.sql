DROP DATABASE truebeauty;
CREATE DATABASE IF NOT EXISTS truebeauty DEFAULT CHARACTER SET latin1;
USE truebeauty;

/*CREACION DE TABLAS*/
CREATE TABLE cita(
    id_cita int unsigned AUTO_INCREMENT NOT NULL,
    fecha_creacion DATE NOT NULL,
    hora time NOT NULL,
    id_servicio int unsigned NOT NULL,
    id_estilista int unsigned NOT NULL,
    id_cliente int unsigned NOT NULL,
    id_sucursal int unsigned NOT NULL,	
    PRIMARY KEY (id_cita)
) ENGINE=MyISAM default char set=latin1;


CREATE TABLE servicio(
    id_servicio int unsigned AUTO_INCREMENT NOT NULL,
    descripcion varchar(150) NOT NULL,
    precio decimal(10,2) NOT NULL,
    tiempo decimal(10,2) NOT null,
    PRIMARY KEY (id_servicio)
)ENGINE=MyISAM default char set=latin1;

CREATE TABLE usuario (
    id_usuario int unsigned AUTO_INCREMENT not null,
    nombre varchar(50) NOT NULL,
    apellido_paterno varchar(50) NOT NULL,
    apellido_materno varchar(50) NOT NULL,
    correo varchar(50) NOT NULL,
    contrasenia varchar(25) NOT NULL,
    telefono int(15),
    tipo_usuario ENUM('gerente','recepcionista','estilista','cliente') NOT NULL,
    PRIMARY KEY (id_usuario)

)ENGINE=MyISAM default char set=latin1;

CREATE TABLE empleado(
    id_empleado int unsigned AUTO_INCREMENT not null,
    id_usuario int unsigned NOT NULL,
    id_sucursal int unsigned,
    turno ENUM('matutino','vespertino','tiempo completo'),
    PRIMARY KEY(id_empleado)

)ENGINE=MyISAM default char set=latin1;

CREATE TABLE sucursal(
    id_sucursal int unsigned AUTO_INCREMENT not null,
    direccion varchar(255),
    telefono int(10),
    id_gerente int unsigned,
    PRIMARY KEY(id_sucursal)

)ENGINE=MyISAM default char set=latin1;

/* CREACION DE LLAVES FORANEAS*/
ALTER TABLE cita ADD FOREIGN KEY(id_cliente) REFERENCES usuario(id_usuario);
ALTER TABLE cita ADD FOREIGN KEY(id_estilista) REFERENCES usuario(id_usuario);
ALTER TABLE cita ADD FOREIGN KEY(id_servicio) REFERENCES servicio(id_servicio);
ALTER TABLE cita ADD FOREIGN KEY(id_sucursal) REFERENCES sucursal(id_sucursal);


ALTER TABLE empleado ADD FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario);
ALTER TABLE empleado ADD FOREIGN KEY(id_sucursal) REFERENCES sucursal(id_sucursal);

ALTER TABLE sucursal ADD FOREIGN KEY(id_gerente) REFERENCES usuario(id_usuario);

/*INSERTS */

INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo, contrasenia, telefono, tipo_usuario)
VALUES('Luis Ernesto','Hernández','López','a220213915@unison.mx','holaxd','6621935761','gerente');

INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo, contrasenia, telefono, tipo_usuario)
VALUES('Admin','Admin','Admin','truebeauty@gmail.com','$5$rounds=535000$656MRtarbYnV5bBM$1kwFoigovLgyRQz/Q/UL0wn61L34fFOhHPkKiZiig62','6621935761','gerente');

