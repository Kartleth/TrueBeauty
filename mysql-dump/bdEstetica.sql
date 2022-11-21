DROP DATABASE truebeauty;
CREATE DATABASE IF NOT EXISTS truebeauty DEFAULT CHARACTER SET latin1;
USE truebeauty;

/*CREACION DE TABLAS*/
CREATE TABLE cita(
    id_cita int unsigned AUTO_INCREMENT NOT NULL,
    fecha DATE NOT NULL,
    hora time NOT NULL,
    hora_fin time,
    id_cliente int unsigned NOT NULL,
    id_sucursal int unsigned NOT NULL,
    monto decimal NOT NULL,
    iva decimal(10,2) unsigned NOT null,
    total decimal(10,2) unsigned NOT null,
    PRIMARY KEY (id_cita)
) ENGINE=MyISAM default char set=latin1;


CREATE TABLE servicio(
    id_servicio int unsigned AUTO_INCREMENT NOT NULL,
    nombre varchar(200) NOT NULL,
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
    contrasenia varchar(200) NOT NULL,
    telefono varchar(15),
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
    nombre varchar(200),
    direccion varchar(255),
    telefono varchar(15),
    id_gerente int unsigned,
    PRIMARY KEY(id_sucursal)

)ENGINE=MyISAM default char set=latin1;

CREATE TABLE estilista_servicio(
    id_estilista int unsigned not null,
    id_servicio int unsigned not null

)ENGINE=MyISAM default char set=latin1;

CREATE TABLE cita_servicio(
    id_cita int unsigned not null,
    id_servicio int unsigned not null,
    id_estilista int unsigned not null,
    hora_inicio time not null,
    hora_fin time not null
)ENGINE=MyISAM default char set=latin1;


/* CREACION DE LLAVES FORANEAS*/
ALTER TABLE cita ADD FOREIGN KEY(id_cliente) REFERENCES usuario(id_usuario);
ALTER TABLE cita ADD FOREIGN KEY(id_sucursal) REFERENCES sucursal(id_sucursal);


ALTER TABLE empleado ADD FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario);
ALTER TABLE empleado ADD FOREIGN KEY(id_sucursal) REFERENCES sucursal(id_sucursal);

ALTER TABLE sucursal ADD FOREIGN KEY(id_gerente) REFERENCES usuario(id_usuario);


ALTER TABLE estilista_servicio ADD FOREIGN KEY(id_estilista) REFERENCES usuario(id_usuario);
ALTER TABLE estilista_servicio ADD FOREIGN KEY(id_servicio) REFERENCES servicio(id_servicio);

ALTER TABLE cita_servicio ADD FOREIGN KEY(id_cita) REFERENCES cita(id_cita);
ALTER TABLE cita_servicio ADD FOREIGN KEY(id_servicio) REFERENCES servicio(id_servicio);
ALTER TABLE cita_servicio ADD FOREIGN KEY(id_estilista) REFERENCES usuario(id_usuario);

/*INSERTS */
use truebeauty;
INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo, contrasenia, telefono, tipo_usuario)
VALUES('Admin','Admin','Admin','truebeauty@gmail.com','$5$rounds=535000$656MRtarbYnV5bBM$1kwFoigovLgyRQz/Q/UL0wn61L34fFOhHPkKiZiig62','6621935761','gerente');
INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo, contrasenia, telefono, tipo_usuario)
VALUES('Luis Ernesto','Hernández','López','a220213915@unison.mx','$5$rounds=535000$656MRtarbYnV5bBM$1kwFoigovLgyRQz/Q/UL0wn61L34fFOhHPkKiZiig62','6621935761','recepcionista');
INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo, contrasenia, telefono, tipo_usuario)
VALUES('David','Nuñez','Gurrola','david@gmail.com','$5$rounds=535000$656MRtarbYnV5bBM$1kwFoigovLgyRQz/Q/UL0wn61L34fFOhHPkKiZiig62','21354684565','estilista');
INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo, contrasenia, telefono, tipo_usuario)
VALUES('Karla','Lerma','Molina','karla@gmail.com','$5$rounds=535000$656MRtarbYnV5bBM$1kwFoigovLgyRQz/Q/UL0wn61L34fFOhHPkKiZiig62','12145789632','cliente');

INSERT INTO sucursal(nombre,direccion, telefono, id_gerente) values ('Villa de seris','Colonia villa de seris, calle isabel #18','6212254887',2);


INSERT INTO servicio(nombre,descripcion, precio, tiempo) VALUES ('Peinado','Peinado de cabello',299.99,45);
INSERT INTO servicio(nombre,descripcion, precio, tiempo) VALUES ('Maquillaje','Pintada de caritas',3499.99,45);
INSERT INTO servicio(nombre,descripcion, precio, tiempo) VALUES ('Facial','Se te lava la mugrosa cara',1499.99,45);
INSERT INTO servicio(nombre,descripcion, precio, tiempo) VALUES ('Corte de cabello','Se le corta la greña para que no parezca loquito',299.99,25);
INSERT INTO servicio(nombre,descripcion, precio, tiempo) VALUES ('Manicura','Se le arregla las uñas',999.99,30);
INSERT INTO servicio(nombre,descripcion, precio, tiempo) VALUES ('Pedicura','Se le arregla las uñas de las patas',999.99,30);

INSERT INTO cita(fecha, hora, hora_fin, id_cliente, id_sucursal,monto,iva,total) VALUES ('2023-10-08','8:30','9:00',4,1,1000,160,1160);
INSERT INTO cita(fecha, hora,hora_fin,  id_cliente, id_sucursal,monto,iva,total) VALUES ('2022-12-10','10:00','12:00',4,1,12021,1923.36,13944.36);
INSERT INTO cita(fecha, hora,hora_fin,  id_cliente, id_sucursal,monto,iva,total) VALUES ('2022-12-10','14:00','16:00',4,1,3000,480,3480);

INSERT INTO empleado(id_usuario,id_sucursal,turno) values(3,1,'tiempo completo');

INSERT INTO estilista_servicio VALUES (3,1);
INSERT INTO estilista_servicio VALUES (3,2);
INSERT INTO estilista_servicio VALUES (3,3);
INSERT INTO estilista_servicio VALUES (3,4);
INSERT INTO estilista_servicio VALUES (3,5);
INSERT INTO estilista_servicio VALUES (3,6);

INSERT INTO cita_servicio VALUES (1,1,3,'10:00','10:45');
INSERT INTO cita_servicio VALUES (1,2,3,'10:45','11:30');
INSERT INTO cita_servicio VALUES (1,5,3,'12:00','12:30');
INSERT INTO cita_servicio VALUES (1,6,3,'12:30','13:00');

-- # SELECT * FROM usuario;
-- # /*Estilistas que trabajan en esa sucursal y ofrecen ese servicio */
-- # SELECT E.id_usuario FROM empleado E, estilista_servicio ES WHERE E.id_usuario=ES.id_estilista AND ES.id_servicio=1 AND E.id_usuario=(SELECT estilista_minimo.id_estilista FROM (SELECT servicios_por_estilista.id_estilista, min(servicios_por_estilista.num_servicios) AS num_servicios FROM (SELECT id_estilista, count(id_estilista) as num_servicios FROM estilista_servicio) as servicios_por_estilista LIMIT 1 ) as estilista_minimo);
-- # /*SELECCIONAR ID_ESTILISTA QUE OFREZCA MENOR NUMERO DE SERVICIOS*/
-- # SELECT estilista_minimo.id_estilista FROM (SELECT servicios_por_estilista.id_estilista, min(servicios_por_estilista.num_servicios) AS num_servicios FROM (SELECT id_estilista, count(id_estilista) as num_servicios FROM estilista_servicio) as servicios_por_estilista LIMIT 1 ) as estilista_minimo;
-- # /*SELECCIONAR citas en a esa hora que hagan ese servicio  */
-- SELECT CS.id_estilista from cita_servicio CS, cita C WHERE C.id_cita=CS.id_cita AND C.fecha='2023-08-12' AND CS.hora_inicio>'8:30' AND CS.hora_fin<'8:30' AND CS.id_estilista=3;
-- # /*SELECCIONAR UN ESTILISTA QUE OFREZCA ESE SERVICIO, TRABAJE EN ESA SUCURSAL,TENGA ESA FECHA Y HORA DISPONIBLE*/
-- # SELECT ES.id_estilista FROM cita C, cita_servicio CS, estilista_servicio ES, empleado E
-- #                        WHERE C.id_cita=CS.id_cita
-- #                          AND CS.id_estilista=ES.id_estilista
-- #                          AND E.id_sucursal=1
-- #                          AND ES.id_servicio=3
-- #                          AND CS.hora_inicio>'13:30'
-- #                          AND CS.hora_fin<'13:30'
-- #                        LIMIT 1;
-- #
-- #
-- # SELECT DISTINCT U.id_usuario FROM usuario U, empleado E, estilista_servicio ES, cita_servicio CS, cita C
-- #                        WHERE U.tipo_usuario='estilista'
-- #                          AND E.id_usuario=U.id_usuario
-- #                          AND E.id_sucursal=1
-- #                          AND ES.id_estilista=E.id_usuario
-- #                          AND ES.id_servicio=2
-- #                          AND CS.id_estilista=U.id_usuario
-- #                          AND C.id_cita=CS.id_cita
-- #                          AND NOT( C.fecha='2022-11-24'
-- #                          AND CS.hora_inicio<'11:00'
-- #                          AND CS.hora_fin>'11:00') LIMIT 1;
/*SELECCIONAR NOMBRE ID, NOMBRE DE SERVICIO, DESCRIPCION, PRECIO, ESTILISTA QUE LO DARA */
-- SELECT cs.id_servicio, S.nombre AS nombre_servicio, S.descripcion ,S.precio ,U.nombre AS nombre_estilista, U.apellido_paterno as apellido1_estilista
-- FROM cita_servicio CS, usuario U, servicio S
-- WHERE CS.id_estilista=U.id_usuario
--   AND CS.id_servicio=S.id_servicio
--   AND CS.id_cita=1;
INSERT INTO servicio (nombre, descripcion, precio, tiempo) VALUES ();
