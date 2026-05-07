--USE projeto_teste;
USE projetoPI;
INSERT INTO eleitores (chave_acesso, nome_completo, titulo_eleitor, cpf_criptografado, mesario, status_voto) 
VALUES 
('JOD1234', 'João do Grau', '123456789012', '12312312312', 0, 0),
('DID4321', 'Diego Dançarino', '987654321012', '12345678910', 1, 0);
SELECT * FROM eleitores;

INSERT INTO candidatos (nome_completo, numero_votacao, nome_partido) 
VALUES 
('Felipão', 244, 'O melhor partido'),
('Rafael Paris', 123, 'Partido FRANÇA'),
('Matheus Sabor Japones', 17, 'Takamassa Nomuro');
SELECT * FROM candidatos;

INSERT INTO registro_logs (data_hora_log, tipo, descricao) 
VALUES(NOW(), 'INFO', 'LOG EXEMPLO');
SELECT * FROM registro_logs;

INSERT INTO tabela_votos (id_candidato, data_hora_voto, protocolo_criptografado) 
VALUES (1, NOW(), '123ABC');
SELECT * FROM tabela_votos;

