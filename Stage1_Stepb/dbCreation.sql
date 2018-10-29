use cfarmer;

-- show tables;

drop table if exists `Message`;
drop table if exists `Timestamp`;
drop table if exists `Time`;
drop table if exists `Date`;
drop table if exists `Person`;
drop table if exists `Location`;
drop table if exists `State`;
drop table if exists `City`;

CREATE TABLE IF NOT EXISTS `City` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(128) NULL DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `State` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(128) NULL DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `Location` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `stateId` INT NULL DEFAULT NULL,
        `cityId` INT NULL DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`cityId`) REFERENCES City(id),
		FOREIGN KEY (`stateId`) REFERENCES State(id),
        UNIQUE (`stateId`, `cityId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `Person` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `idStr` VARCHAR(8) NULL DEFAULT NULL,
        `name` VARCHAR(128) NULL DEFAULT NULL,
        `locationId` INT NULL DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`locationId`) REFERENCES Location(id),
        UNIQUE (`idStr`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `Date` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `value` DATE NULL DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE (`value`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `Time` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `value` TIME NULL DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE (`value`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `Timestamp` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `dateId` INT NULL DEFAULT NULL,
        `timeId` INT NULL DEFAULT NULL,
        PRIMARY KEY (`id`),
		FOREIGN KEY (`dateId`) REFERENCES Date(id),
        FOREIGN KEY (`timeId`) REFERENCES Time(id),
        UNIQUE (`dateId`, `timeId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE IF NOT EXISTS `Message` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `value` VARCHAR(512) NULL DEFAULT NULL,
        `personId` INT NULL DEFAULT NULL,
        `timestampId` INT NULL DEFAULT NULL,
        PRIMARY KEY (`id`),
		FOREIGN KEY (`personId`) REFERENCES Person(id),
        FOREIGN KEY (`timestampId`) REFERENCES Timestamp(id))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;
