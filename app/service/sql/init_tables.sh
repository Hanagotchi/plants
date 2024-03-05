#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "plants" <<-'EOSQL'
    CREATE SCHEMA IF NOT EXISTS dev;

    CREATE TABLE IF NOT EXISTS dev.plant_types (
        botanical_name VARCHAR(70) PRIMARY KEY,
        id INT UNIQUE NOT NULL,
        common_name VARCHAR(70) NOT NULL,
        description VARCHAR(1000) NOT NULL,
        cares VARCHAR(1000) NOT NULL,
        photo_link VARCHAR(160) NOT NULL
    );

    DO $do$
    BEGIN
        IF (SELECT COUNT(*) FROM dev.plant_types) = 0 THEN
            INSERT INTO dev.plant_types (botanical_name, id, common_name, description, cares, photo_link)
            VALUES 
                 (
                'Passiflora caerulea',
                1,
                'Passiflora',
                'Es una enredadera ornamental de rápido crecimiento que produce flores exóticas y llamativas. Sus flores son de color blanco y púrpura, con un centro de filamentos que le otorgan un aspecto distintivo y hermoso. Es apreciada tanto por su belleza como por su fragancia, y es comúnmente cultivada en jardines como planta trepadora. Además de su valor ornamental, algunas variedades de Passiflora caerulea también producen frutos comestibles.',
                'La pasionaria no soporta bien la falta de agua, por lo que la tierra debe mantenerse constantemente húmeda. Tampoco se desarrolla bien en suelos húmedos con exceso de agua, por lo que hay que tener en cuenta la retención de agua del suelo.
Florece en ambientes soleados, mostrando preferencia por los lugares con exposición solar continua. Idealmente requiere más de seis horas de luz solar diarias, aunque puede soportar un mínimo de tres horas diarias.
Al ser originaria de regiones subtropicales requiere una temperatura mínima de 15 ℃ para prosperar. Prefiere temperaturas entre 15 y 38 ℃, pero puede tolerar temperaturas más altas con un riego adecuado y al abrigo del sol directo. En los meses más fríos, ajuste la temperatura proporcionando calor suplementario o traslade la planta al interior, a una zona más cálida.
',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/348108976252420096.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Kalanchoe daigremontiana',
                2,
                'Aranto',
                'Planta suculenta que se distingue por sus hojas carnosas y dentadas de color verde oscuro. Lo más notable de esta planta es su capacidad para producir pequeñas plántulas a lo largo de los bordes de las hojas, que caen al suelo y se enraízan fácilmente, lo que le da un aspecto único y llamativo.',
                'En cuanto al riego, deje que el suelo se seque entre riegos brindando agua suficiente pero sin acumulación.
La planta aranto prospera con sol abundante y agradece la mayor cantidad de luz solar posible. Se las arregla bien en zonas con picos de sol con idealmente seis horas de luz directa por día. Puede sobrevivir con una exposición al sol ligeramente reducida (hasta tres horas), pero maximizar la luz solar es lo mejor para un crecimiento sano.
La aranto prefiere un entorno de crecimiento con temperaturas que oscilen entre 20 y 25℃. Sin embargo, puede adaptarse bien a temperaturas que oscilen entre 20 y 38℃ siempre que no esté expuesta a calor extremo o heladas. Durante los meses más fríos, se recomienda mantener la planta en un lugar más cálido o utilizar una lámpara de calor.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/153412761521487877.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Dracaena fragrans',
                3,
                'Palo de Brasil',
                'Planta de interior popular apreciada por su follaje verde oscuro y brillante, que puede tener franjas amarillas o blancas a lo largo de los bordes. Es una planta de crecimiento vertical que puede alcanzar alturas impresionantes',
                'En comparación con otras plantas de interior, palo de Brasil requiere poca agua. Basta con regar la planta una vez a la semana, o cuando la superficie de la maceta esté seca.
La palo de Brasil tiene preferencia por el sol parcial (entre 3 y 6 horas de luz directa por día) pero puede adaptarse a una amplia gama de condiciones de luz solar, incluido el pleno sol y la sombra total. Nada más se deben evitar los cambios extremos de exposición a la luz.
Requiere temperaturas entre 20 y 41 ℃ para prosperar. Prefiere un entorno cálido constante y debe mantenerse a temperaturas superiores a 15,6 ℃ durante los meses más fríos. Durante los calurosos meses de verano, puede beneficiarse de la sombra parcial y el aumento de la humedad para evitar quemaduras en las hojas. ',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/154131794881413123.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Thunbergia alata',
                4,
                'Susana de Ojos negros',
                'Es una planta trepadora con hojas verdes en forma de corazón y flores en forma de trompeta en colores vibrantes como naranja, amarillo y rojo, con un centro oscuro. ',
                'Prospera con abundante luz solar, procedente de entornos abiertos. Asegúrese de que reciba una amplia cantidad de sol al día para promover un crecimiento adecuado. Soporta una sombra mínima cuando es necesario, pero favorece los lugares soleados para una salud óptima.
El hábito de temperatura de susana de Ojos negros requiere un entorno de crecimiento cálido de 20 a 38℃ para prosperar. Regarla regularmente para que crezca mejor.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/153776596791066668.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Tradescantia zebrina',
                5,
                'Zebrina',
                'Esta planta es conocida por sus hojas alargadas de color verde oscuro con franjas plateadas y púrpuras en forma de zebra, lo que le da su nombre.',
                'A la Zebrina le gusta la humedad, pero no debe encharcarse.
Ama la luz. La luz insuficiente conducirá al crecimiento excesivo y a las hojas amarillas, pero la luz intensa quemará las plantas. Si está demasiado sombreado, el zebrina también crecerá mal, con hojas delgadas y flores pequeñas, lo que hará que sea mejor cultivar la planta en un lugar semi sombreado.
Es originaria de regiones tropicales y requiere un rango de temperatura cálido y húmedo de 20 a 38 ℃ para un crecimiento óptimo.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/202694289978032128.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Setcreasea pallida',
                6,
                'Amor de hombre',
                'Esta planta es originaria de México y es apreciada por sus llamativas hojas de color púrpura oscuro. Tiene un crecimiento rastrero y puede producir pequeñas flores rosadas o blancas en ciertas condiciones.',
                'A la Amor de hombre le gusta la humedad, pero no debe encharcarse. También debe estar expuesta a una luz solar intensa pero que no incida directamente sobre ella.
Para que esta planta tropical prospere, querrá mantenerlas entre 25-32℃.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/153715934672977954.jpeg?x-oss-process=image/format,webp/resize,s_340&v=1.3'
            ),
            (
                'Duranta erecta',
                7,
                'Duranta',
                'Es un arbusto ornamental originario de América tropical que se caracteriza por sus racimos de pequeñas flores azules o moradas seguidas de pequeñas bayas doradas. Las hojas son verde brillante y tienen un aspecto denso y frondoso. La Duranta es popular en paisajismo
debido a su follaje atractivo y sus brillantes bayas.',
                'Duranta requiere mucha agua para su atractiva floración, pero regarla en exceso puede dañar su salud. En climas cálidos, se recomienda regar la planta unas dos veces por semana en verano y una vez cada dos semanas en la estación fría.
Prospera en zonas con abundante sol, ya que procede de entornos con amplia exposición a la luz solar. Sin embargo, también puede adaptarse a zonas con algo menos de luz solar. Proporcionarle el sol adecuado es vital para un crecimiento óptimo y una floración vibrante.
Está bien adaptado a climas cálidos y puede prosperar fácilmente en temperaturas entre 26 °C y 35 °C. También continuará creciendo en temperaturas superiores a 40 °C. Sin embargo, duranta tendrá dificultades si la temperatura cae por debajo de los 4 °C y las heladas pueden matarlo.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/348114628429381632.jpeg?x-oss-process=image/format,webp/resize,s_340&v=1.3'
            ),
            (
                'Acer negundo',
                8,
                'Arce Negundo',
                'Tiene hojas compuestas de color verde claro que se vuelven amarillas en otoño. Produce pequeñas flores amarillas verdosas en primavera, seguidas de samaras aladas que maduran en otoño.',
                'Arce negundo prefiere que la tierra se mantenga húmeda, especialmente en verano, porque el clima seco puede provocar que sus hojas se quemen o incluso se caigan. En verano, además de regar las raíces, se recomienda rociar el follaje por la noche para aumentar la humedad. En invierno, basta con asegurarse de que la tierra no se seque.
Prospera en zonas con abundante exposición al sol, ya que es nativa de entornos con abundante luz. Puede adaptarse a lugares moderadamente soleados si es necesario. Para un crecimiento óptimo, asegúrese de que esta planta recibe abundante luz solar a lo largo del día.
El arce negundo prefiere un rango de temperaturas de 0 a 35 ℃. Crece de forma natural en climas templados y puede adaptarse bien a diferentes temperaturas extremas.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/153410240375685143.jpeg?x-oss-process=image/format,webp/resize,s_340&v=1.3'
            ),
            (
                'Tropaeolum majus',
                9,
                'Capuchina',
                'Es una planta anual originaria de América del Sur que se cultiva por sus brillantes flores y sus hojas redondeadas en forma de escudo. Las flores pueden ser de varios colores, incluyendo naranja, amarillo, rojo y rosa, y tienen un aspecto característico en forma de sombrero o capucha, de ahí su nombre común.',
                'Es muy importante mantener regada su capuchina, especialmente durante los periodos secos. La capuchina y sus flores se beneficiarán enormemente de un riego regular, que debe realizarse una o dos veces por semana, dependiendo de las condiciones climáticas.
La capuchina prospera cuando está expuesta a abundante luz solar, ya que es originaria de hábitats soleados. Para garantizar un crecimiento sano, necesita una generosa dosis de sol diaria, aunque puede arreglárselas en condiciones de ligera sombra cuando es necesario.
Requiere una temperatura cálida para desarrollarse, siendo su entorno de crecimiento nativo en zonas de pleno sol y temperaturas suaves que oscilan entre 15℃ y 38℃. No tolera temperaturas inferiores a 10℃.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/348114628429381632.jpeg?x-oss-process=image/format,webp/resize,s_340&v=1.3'
            ),
           (
                'Arum italicum',
                10,
                'Tragontina',
                'Es una planta perenne que se distingue por sus hojas grandes y en forma de flecha de color verde oscuro con venas blancas prominentes. Produce espádices amarillos o verdes rodeados por una bráctea en forma de embudo llamada espata, que puede ser de color blanco cremoso. Esta planta es apreciada tanto por su follaje decorativo como por sus inflorescencias inusuales.',
                'Tiene un requerimiento de agua promedio, necesita agua regularmente pero sin acumulación. Necesita entre 3 y 6 horas diarias de luz solar directa para desarrollarse. Sin embargo, también necesita algo de sombra durante las horas más calurosas del día para evitar los daños del sol.
La mejor temperatura para Tragontina debe oscilar entre 18 y 27℃. Las temperaturas más altas pueden causar marchitamiento, caída e incluso quemaduras solares en las hojas, de las que puede recuperarse con dificultad. ',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/352294194249170944.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Lagerstroemia indica',
                11,
                'Árbol de Júpiter',
                'Sus flores pueden ser rosadas claras o blancas, y la forma en que crecen asemeja un racimo de uvas.',
                'Después de plantarlas, las árbol de Júpiter deben regarse a fondo inmediatamente y, a continuación, una vez cada 3-5 días.
El árbol de Júpiter como luz solar plena y son ligeramente tolerantes a la sombra. Requieren mucha luz para crecer vigorosamente y florecer en grandes cantidades. Seleccione un campo con 6-8h de luz solar directa al día, como un espacio abierto en un jardín, y evite la sombra de cercas altas, edificios y otros árboles
Requiere una temperatura entre 10 y 35 ℃, que es la adecuada en su entorno de crecimiento nativo.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/201214506240704512.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Monstera deliciosa',
                12,
                'Monstera',
                'Es conocida por sus hojas grandes y espectaculares con perforaciones naturales, que le dan un aspecto único y distintivo. Esta planta trepadora puede alcanzar alturas significativas cuando se cultiva en condiciones adecuadas. Además de su atractivo ornamental, la Monstera deliciosa produce frutos comestibles, aunque tardan varios meses en madurar completamente.',
                'La Monstera necesita una cantidad media de agua. Es importante evitar regar la planta en exceso, ya que esto puede provocar la pudrición de las raíces. Debe regarla una vez a la semana, aunque puede necesitar un riego adicional cuando hace calor,o cuando la tierra está ligeramente seca. A monstera deliciosa le gusta un entorno húmedo, así que, además de regarla, rocía ligeramente las hojas cada dos días para evitar que la planta se seque.
Ama los lugares soleados de su hogar. Se recomienda que coloque su monstera en un lugar que reciba mucha luz solar indirecta con un poco de sombra parcial.
Prosperará en un ambiente cálido con alta humedad. Se puede cultivar en jardines pero generalmente es una planta de interior con temperaturas entre 18-30 °C idealmente. Si la temperatura desciende por debajo de los 15 °C , comenzará a morir.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/347088479137988608.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Rosa chinensis',
                13,
                'Rosa china',
                'Es originaria de Asia y es apreciada por sus grandes y vistosas flores de colores brillantes que pueden ser rojas, rosas, naranjas, amarillas o blancas, dependiendo de la variedad. Estas flores tienen cinco pétalos prominentes y un estambre central. Las hojas son de color verde oscuro y pueden ser ovaladas o lobuladas.',
                'Le gustan los entornos húmedos pero no inundados de agua, por lo que es importante mantener la tierra bien drenada, ya se plante en el suelo o en maceta.
La planta prefiere el sol completo, aunque también tolera un medio de sombra parcial. Si está parcialmente a la sombra, normalmente solo le surgen hojas y no florece. Le gustan los entornos frescos y ventilados y no tolera las altas temperaturas. El rango de temperatura óptimo es 15 a 26 ℃.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/202648501331689472.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Coleus scutellarioides',
                14,
                'Cóleo',
                'Es una planta herbácea perenne originaria de regiones tropicales de Asia y África. Tiene vistosas hojas multicolores, suaves y de formas variadas. Los colores que pueden incluir combinaciones de verde, rojo, rosa, amarillo, blanco y púrpura, creando un efecto visual llamativo.',
                'Cóleo prospera en condiciones cálidas y húmedas (21 a 37 ℃). Es fundamental regarla con moderación y regularidad. En interior riéguela cada dos o tres días. Cuando la temperatura exterior sea alta, riéguela con más frecuencia. Si las hojas se caen hay que regar más. Las hojas que amarillean pueden ser un indicio de riego excesivo.
Una ubicación parcialmente sombreada es ideal para el crecimiento de las plantas. Si la planta está perdiendo las hojas, es una señal de que hay muy poco sol o de que hace demasiado frío. Las temperaturas inferiores a 10 ℃ evitarán su crecimiento. Si la temperatura cae por debajo de 7 ℃ , morirá.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/152432134588465153.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Haworthia fasciata',
                15,
                'Cebra',
                'Es una planta suculenta nativa de Sudáfrica. Se caracteriza por sus rosetas de hojas gruesas y carnosas que forman una forma compacta y esférica. Las hojas son de color verde oscuro y están marcadas con bandas blancas o plateadas a lo largo de los márgenes, lo que le da un aspecto distintivo de rayas.',
                'La planta cebra disfruta de abundante sol, idealmente una mezcla de exposición total y parcial. Debe regarse moderadamente.
Es originaria de zonas con temperaturas más cálidas y prefiere temperaturas entre20 y 38 ℃.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/154206673341251610.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Echeveria secunda',
                16,
                'Tememetla',
                'Es una suculenta de crecimiento rastrero que tiende a crecer formando pequeñas colonias ordenadas y compactas. Carece de tallo y las hojas se agrupan en torno a una roseta central, donde crecen los hijuelos.',
                'No necesita mucha agua. Necesita luz brillante, transparente y dispersa aunque la fuerte luz solar del verano puede quemar sus hojas y tallos haciendo que crezca muy lentamente.
Crece en temperaturas suaves en primavera y otoño y no puede resistir el frío extremo.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/153783670602203146.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Sansevieria trifasciata',
                17,
                'Lengua de tigre',
                'Suculenta de interior apreciada por su aspecto elegante y fácil mantenimiento. Tiene hojas gruesas y erectas que crecen verticalmente desde una base basal. Las hojas son de color verde oscuro y tienen patrones de bandas amarillas o plateadas a lo largo de los bordes.',
                'La sansevieria es una planta bastante tolerante a la sequía, que solo requiere tierra húmeda en primavera y verano y no le gusta que la tierra esté demasiado húmeda. En general, debe regarse dos veces por semana con una frecuencia reducida de riego durante su período de latencia invernal.
Prefiere el sol parcial, pero puede soportar tanto la luz solar intensa como la luz mínima. Evite la sobreexposición a los rayos abrasadores para prevenir daños en las hojas.
En su entorno de crecimiento nativo, sansevieria prospera a temperaturas que oscilan entre 20 y 41 ℃. Prefiere temperaturas cálidas entre 21 y 32 ℃, pero puede tolerar temperaturas bajas de hasta 10 ℃ en períodos breves. Para un crecimiento óptimo, mantenga un rango de temperatura de 18 a 27 ℃. Durante los meses de invierno, reduzca el riego y mantenga la planta en un ambiente más fresco, en torno a 10 a 15 ℃.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/153936867790684172.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Epipremnum aureum',
                18,
                'Potus',
                'Tiene hojas brillantes y en forma de corazón que crecen en tallos largos y colgantes, lo que la convierte en una excelente opción para colgar en cestas o macetas elevadas. Las hojas son de color verde intenso, aunque hay variedades con patrones de moteado o variegado en tonos de blanco, amarillo o crema.',
                'Requiere un ambiente húmedo. Mantenga un poco húmeda la tierra de la maceta en primavera, verano y otoño. Riegue el potus todos los días en verano. No riegue cuando la temperatura sea alta al mediodía, sino por la mañana o por la tarde. Riegue una vez cada 4-5 días en primavera y otoño. En inviero regar cuando la superficie esté seca únicamente.
Es una planta poco luminosa. Prospera en condiciones de sombra, aunque tolera algo de sol filtrado. Evite la luz solar intensa para evitar que las hojas se quemen y mantener un follaje exuberante. Las temperaturas no deberían caer por debajo de 10 ℃ , pero su rango preferido es entre 20 a 30 ℃.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/152347936049594370.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Crassula ovata',
                19,
                'Árbol de jade',
                'El árbol de jade es una suculenta que se usa de forma ornamental en jardines de rocas y grandes macetas porque puede alcanzar la increíble altura de 2 m. Debido a su porte arbustivo, se puede cultivar como si fuera un bonsái. El increíble tono verde de su follaje recuerda al del mineral de jade.',
                'No necesita mucha agua. Regar únicamente cuando la tierra esté seca.
La árbol de jade prefiere un equilibrio entre sol y sombra, prosperando en condiciones de luz moteada. Su hábitat nativo incluye zonas con luz solar difusa. Para favorecer un crecimiento sano, evite las zonas con excesiva exposición al sol o sombra profunda continua.
La temperatura de crecimiento adecuada de árbol de jade es superior a 15 ℃ , y puede crecer normalmente en primavera, verano y otoño. Puede tolerar altas temperaturas , pero entrará en el período de latencia cuando la temperatura sea superior a 33 ℃.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/152346179407970311.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Kalanchoe blossfeldiana',
                20,
                'Kalanchoe',
                'Kalanchoe blossfeldiana es una planta suculenta perenne originaria de Madagascar que es popular por sus brillantes y coloridas flores. Sus hojas son carnosas y de un verde intenso, y produce racimos densos de flores en una variedad de tonos, incluyendo rojo, rosa, naranja, amarillo y blanco. Estas flores están formadas por pequeñas flores tubulares agrupadas en umbelas.',
                'Kalanchoe no necesita mucha agua. Regar únicamente cuando la tierra esté seca.
Muestra preferencia por la luz solar abundante, prosperando en lugares con amplia exposición. Acostumbrada originalmente a hábitats con intensidad solar variable, esta especie adaptable también puede crecer en condiciones más sombrías. Para un crecimiento óptimo, proporcione rayos generosos pero no abrasadores.
Su entorno de crecimiento nativo requiere temperaturas de alrededor de 20 a 27 ℃. Sin embargo, puede tolerar temperaturas que oscilen entre 10 y 38 ℃. Para un crecimiento óptimo, prefiere temperaturas en torno a 20 a 30 ℃ (68 a 86 ℉). Durante el invierno, puede adaptarse a temperaturas más bajas siempre que se mantenga alejada de corrientes de aire y vientos fríos.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/153754456234655761.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Portulaca oleracea',
                21,
                'Verdolaga',
                'Es una hierba postrada de aspecto suculento, muy notable por la rapidez de su crecimiento y sus tallos y ramas completamente lisos. Es invasora y tóxica para humanos y animales.',
                'La verdolaga prospera con abundante sol, disfrutando de al menos seis horas diarias. Para un crecimiento óptimo, asegúrese un lugar soleado y evite la sombra excesiva.
Verdolaga puede cultivarse en una amplia gama de temperaturas, de 0 a 38 ℃. Esta planta adaptable es originaria de regiones cálidas y secas, y prefiere pleno sol y un suelo que drene bien.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/201222563599351808.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            ),
            (
                'Canna indica',
                22,
                'Caña de las indias',
                'La caña de las indias es una planta herbácea rizomatosa que se cultiva como ornamental en parques y jardines. Tiene tallos erectos con hojas grandes alternas y flores de color rojo a amarillo anaranjado. ',
                'Aunque a la caña de las indias le gusta el suelo húmedo, algunas variedades no soportar estar encharcadas mucho tiempo, puesto que su raíz se puede pudrir. Por lo general, se requiere regarlas una vez a la semana en zonas donde las precipitaciones no superen 2,5 cm por semana.
Prospera con sol abundante, ya que procede de hábitats bañados por el sol. Las condiciones ideales incluyen una exposición constante a la luz solar; sin embargo, puede soportar zonas ligeramente sombreadas si es necesario. Evite la sombra prolongada para un crecimiento óptimo.
Su temperatura de crecimiento adecuada es entre 16 a 30 ℃ y la temperatura ambiente no debe ser inferior a los 10 ℃.',
                'https://www.picturethisai.com/image-handle/website_cmsname/image/1080/154076621731528708.jpeg?x-oss-process=image/format,webp/resize,s_422&v=1.3'
            );
        END IF;
    END
    $do$;

    CREATE TABLE
        IF NOT EXISTS dev.plants (
            id SERIAL PRIMARY KEY,
            id_user INT NOT NULL,
            name VARCHAR(64) NOT NULL,
            scientific_name VARCHAR(70) NOT NULL,
            CONSTRAINT fk_plant_type
                FOREIGN KEY (scientific_name)
                    REFERENCES dev.plant_types(botanical_name)

    );

    DO $do$ BEGIN
        IF (SELECT COUNT(*) FROM dev.plants) = 0 THEN
            INSERT INTO dev.plants (id_user, name, scientific_name) VALUES
                (1, 'Lengua', 'Sansevieria trifasciata'),
                (2, 'Rosa', 'Rosa chinensis'),
                (3, 'Flor', 'Passiflora caerulea');
        END IF;
    END $do$;

    CREATE OR REPLACE FUNCTION trigger_set_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TABLE IF NOT EXISTS dev.logs (
        id SERIAL PRIMARY KEY, 
        title VARCHAR(200) NOT NULL, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        content VARCHAR(1000) NOT NULL,
        plant_id INT,
        CONSTRAINT fk_plant
            FOREIGN KEY (plant_id)
                REFERENCES dev.plants(id)
    );

    CREATE TRIGGER set_timestamp
    BEFORE UPDATE ON dev.logs
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

    CREATE TABLE IF NOT EXISTS dev.logs_photos (
        id SERIAL PRIMARY KEY,
        log_id INT,
        photo_link VARCHAR(120) NOT NULL, 
        CONSTRAINT fk_log
            FOREIGN KEY (log_id)
                REFERENCES dev.logs(id)
    );

EOSQL
