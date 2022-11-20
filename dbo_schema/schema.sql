drop table if exists usuario;
create table usuario (
    id integer primary key autoincrement,
    nome varchar(255) not null,
    email varchar(255) not null,
    login varchar(255) unique not null,
    senha varchar(255) not null
);

drop table if exists cartao_rfid;
create table cartao_rfid (
    id integer primary key autoincrement,
    usuario_id integer not null,
    numero_cartao varchar(255) not null,

    FOREIGN KEY(usuario_id) REFERENCES usuario(id)
);