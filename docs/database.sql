CREATE DATABASE IF NOT EXISTS projetoPI;
--USE projeto_teste;
--show DATABASES;

USE projetoPI;

CREATE TABLE eleitores (
	id INT PRIMARY KEY AUTO_INCREMENT,
    chave_acesso VARCHAR(200) NOT NULL,
    nome_completo VARCHAR(50) NOT NULL,
    titulo_eleitor VARCHAR(12) NOT NULL,
    cpf_criptografado VARCHAR(30) NOT NULL UNIQUE,
    mesario BOOLEAN NOT NULL,
    status_voto BOOLEAN NOT NULL
);

CREATE TABLE candidatos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    nome_completo VARCHAR(50) NOT NULL,
    numero_votacao INT NOT NULL,
    nome_partido VARCHAR(20),
    foto_ascii VARCHAR(255)
);

CREATE TABLE registro_logs (
	id_log INT PRIMARY KEY AUTO_INCREMENT,
    data_hora_log DATETIME NOT NULL,
    tipo VARCHAR(15) NOT NULL,
    descricao VARCHAR(50)
);


CREATE TABLE tabela_votos (
	id_voto INT PRIMARY KEY AUTO_INCREMENT,
    id_candidato INT NOT NULL,
    data_hora_voto DATETIME NOT NULL,
    protocolo_criptografado VARCHAR(30) NOT NULL,
    FOREIGN KEY (id_candidato) REFERENCES candidatos(id)
);
