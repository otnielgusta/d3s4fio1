DROP TABLE IF EXISTS `endereco`;

CREATE TABLE `endereco` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pais` varchar(45) NOT NULL,
  `estado` varchar(45) NOT NULL,
  `municipio` varchar(45) NOT NULL,
  `cep` varchar(9) NOT NULL,
  `rua` varchar(10) NOT NULL,
  `numero` int DEFAULT NULL,
  `complemento` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO `endereco` VALUES (1,'Brasil','Minas Gerais','Braúnas','35189000','Longino',19,'Casa');

DROP TABLE IF EXISTS `usuario`;

CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `idEndereco` int NOT NULL,
  `cpf` varchar(11) NOT NULL,
  `pis` varchar(20) NOT NULL,
  `senha` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idEndereco` (`idEndereco`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`idEndereco`) REFERENCES `endereco` (`id`)
);

INSERT INTO `usuario` VALUES (1,'Otniel Silva Santos','otnielsilvag4@gmail.com',1,'10606959602','1234567','teste');
