CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.plant_types (
    botanical_name VARCHAR(70) PRIMARY KEY, 
    common_name VARCHAR(70) NOT NULL, 
    description VARCHAR(600) NOT NULL,
    cares VARCHAR(600) NOT NULL, 
    photo_link VARCHAR(120) NOT NULL
);

DO
$do$
BEGIN
    IF (SELECT COUNT(*) FROM dev.plant_types) = 0 THEN
        INSERT INTO dev.plant_types (botanical_name, common_name, description, cares, photo_link) VALUES 
            (
                'Streptocarpus', 
                'Cabo Primrose',
                'Su nombre común es Cabo Primrose, refiriéndose al nombre de varias especies de Sudáfrica y su semejanza superficial al género Primula. El género es nativo de partes de África y Madagascar (con unas pocas especies extrañas en Asia, que probablemente no tienen cabida en el género). Las plantas a menudo crecen en la sombra de las laderas rocosas o acantilados. Se encuentran cada vez más sobre el terreno, grietas de rocas, y la semilla puede germinar y crecer casi en cualquier parte.',
                'Se desempeña mejor con luz brillante filtrada y sombra del sol abrasador en suelos fértiles, húmedos, ricos en humus y bien drenados. Riegue libremente permitiendo que la tierra se seque entre riegos. Alimente quincenalmente con un fertilizante con alto contenido de potasio.',
                'https://www.whiteflowerfarm.com/mas_assets/cache/image/3/e/e/2/16098.Jpg'
            ),
            (
                'Pilea microphylla',
                'Helecho Artilleria',
                'Es una planta anual originaria de Florida, México, las Indias Occidentales y América Central y del Sur tropical. La planta pertenece a la familia Urticaceae.​ Tiene tallos de color verde claro, casi suculentos, y pequeñas hojas de 1/8 que contribuyen a su otro apodo, Helecho Artillería, aunque no está relacionado con los helechos.',
                'Utilice tierra para macetas rica en materia orgánica, suelta, con buen drenaje y que retenga la humedad. Evite compactar la tierra con fuerza al plantar. En su lugar, apisónelo sin apretar y deje muchos orificios de aire para facilitar el flujo de nutrientes, oxígeno y agua. Fertilice con moderación para evitar la acumulación de sales y enjuague varias veces según sea necesario en caso de sobrealimentación. Mantenga una humedad uniforme sin sobresaturación regando cuando la superficie del suelo se sienta seca.',
                'https://gardenerspath.com/wp-content/uploads/2022/03/How-to-Grow-Artillery-Plant-Hero.jpg'
            ),
            (
                'Pentas lanceolata',
                'Estrella egipcia',
                'Es una especie de planta con flores (Angiosperma) perteneciente a la familia Rubiaceae, es nativa de gran parte de África así como de Yemen.​ Es conocida por su amplio uso como planta de jardín donde a menudo se la usa en los jardines para mariposas.',
                'Si reciben abono para plantas de flor durante el periodo productivo y se pinzan las flores marchitas, la producción será más abundante. Se han de podar al final del invierno para que puedan rebrotar con fuerza. Las pentas pueden verse afectadas por los pulgones y la araña roja, que suelen combatirse con el mismo fitosanitario.',
                'https://www.verdeesvida.es/inc/timthumb.php?src=/files/plant/19082014112356_Pentas.jpg&w=600'
            ),
            (
                'Ixora coccinea',
                'Planta coral',
                'Es un pequeño arbusto con numerosas flores de pequeño tamaño que permanecen formando umbelas compuestas durante casi todo el año. Es originaria de Asia, específicamente del sur de la India y de Sri Lanka y es muy empleada en jardinería.',
                'Requiere sol y agua en abundancia y es más feliz al aire libre a pleno sol y en un ambiente adecuadamente húmedo. Cuando se cultiva en interiores, se deben mantener estas condiciones subtropicales que conducirán a una planta de interior de Ixora coccinea saludable que florecerá durante todo el año.',
                'https://cdn0.ecologiaverde.com/es/posts/3/4/8/planta_ixora_cuidados_1843_orig.jpg'
            );
    END IF;
END
$do$;