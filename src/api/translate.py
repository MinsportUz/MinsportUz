import re

retranslit_words = {'mesenat': 'меценат', 'nuqtayi nazar': 'нуқтаи назар', 'biolyuminessensiya': 'биолюминесценция',
                    'differensiatsiya': 'дифференциация', 'gallyutsinatsiya': 'галлюцинация',
                    'teleinssenirovka': 'телеинсценировка', 'lyuminessensiya': 'люминесценция',
                    'rekognossirovka': 'рекогносцировка', 'sitodiagnostika': 'цитодиагностика',
                    'broneavtomobil': 'бронеавтомобил[ь]', 'dissotsiatsiya': 'диссоциация',
                    'nitroglitserin': 'нитроглицерин', 'shtangensirkul': 'штангенциркул[ь]',
                    'alma-terapiya': 'альма-терапия', 'avtomagistral': 'автомагистрал[ь]',
                    'geliotsentrik': 'гелиоцентрик', 'koeffitsiyent': 'коэффициент', 'politsmeyster': 'полицмейстер',
                    'predoxranitel': 'предохранител[ь]', 'radiospektakl': 'радиоспектакл[ь]',
                    'reemigratsiya': 'реэмиграция', 'reevakuatsiya': 'реэвакуация', 'sivilizatsiya': 'цивилизация',
                    'devalvatsiya': 'девальвация', 'inssenirovka': 'инсценировка', 'kapelmeyster': 'капельмейстер',
                    'kinofestival': 'кинофестивал[ь]', 'kinossenariy': 'киносценарий', 'levomitsetin': 'левомицетин',
                    'pulverizator': 'пульверизатор', 'revalvatsiya': 'ревальвация', 'sutemizuvchi': 'сутэмизувчи',
                    'viklyuchatel': 'виключател[ь]', 'yuriskonsult': 'юрисконсульт', 'avtopritsep': 'автоприцеп',
                    'bakteritsid': 'бактерицид', 'brutsellyoz': 'бруцеллёз', 'feldmarshal': 'фельдмаршал',
                    'geotsentrik': 'геоцентрик', 'glyatsiolog': 'гляциолог', 'kinokonsert': 'киноконцерт',
                    'konferansye': 'конферансье', 'mikroinsult': 'микроинсульт', 'monokultura': 'монокультура',
                    'penitsillin': 'пенициллин', 'press-papye': 'пресс-папье', 'retsipiyent': 'реципиент',
                    'shmutstitul': 'шмуцтитул', 'vklyuchatel': 'включател[ь]', 'xoletsistit': 'холецистит',
                    'adyunktura': 'адъюнктура', 'bolshevizm': 'большевизм', 'bronenoses': 'броненосец',
                    'cherepitsa': 'черепица', 'eskadrilya': 'эскадрилья', 'fizkultura': 'физкультура',
                    'fortepyano': 'фортепьяно', 'fotoatelye': 'фотоателье', 'giposulfit': 'гипосульфит',
                    'gipotsentr': 'гипоцентр', 'gorizontal': 'горизонтал[ь]', 'gotovalniy': 'готовальний',
                    'kanserogen': 'канцероген', 'kastryulka': 'кастрюлька', 'kolonsifra': 'колонцифра',
                    'konsepsiya': 'концепция', 'konsessiya': 'концессия', 'korrupsiya': 'коррупция',
                    'litsenziya': 'лицензия', 'marselyeza': 'марсельеза', 'menshevizm': 'меньшевизм',
                    'mikrorayon': 'микрорайон', 'mizanssena': 'мизансцена', 'munitsipal': 'муниципал',
                    'oftalmolog': 'офтальмолог', 'palpatsiya': 'пальпация', 'pochtalyon': 'почтальон',
                    'pulmonolog': 'пульмонолог', 'qaynegachi': 'қайнэгачи', 'retsenzent': 'рецензент',
                    'retsenziya': 'рецензия', 'sellyuloza': 'целлюлоза', 'sentrifuga': 'центрифуга',
                    'sitologiya': 'цитология', 'ssintigraf': 'сцинтиграф', 'tendensioz': 'тенденциоз',
                    'uborshitsa': 'уборшица', 'valeryanka': 'валерьянка', 'valvatsiya': 'вальвация',
                    'violonchel': 'виолончел[ь]', 'xolodilnik': 'холодильник', 'aryergard': 'арьергард',
                    'atsetilen': 'ацетилен', 'avianoses': 'авианосец', 'avtomobil': 'автомобил[ь]',
                    'biomitsin': 'биомицин', 'bolshevik': 'большевик', 'byulleten': 'бюллетен[ь]',
                    'epitsentr': 'эпицентр', 'feldyeger': 'фельдъегер[ь]', 'fotoalbom': 'фотоальбом',
                    'geraldika': 'геральдика', 'gerbitsid': 'гербицид', 'glitserin': 'глицерин', 'gorchitsa': 'горчица',
                    'gusenitsa': 'гусеница', 'inyeksiya': 'инъекция', 'katapulta': 'катапульта',
                    'kompanyon': 'компаньон', 'kompyuter': 'компьютер', 'konferens': 'конференц',
                    'konfutsiy': 'конфуций', 'konslager': 'концлагер[ь]', 'kulturizm': 'культуризм',
                    'lyutetsiy': 'лютеций', 'magistral': 'магистрал[ь]', 'meditsina': 'медицина',
                    'menshevik': 'меньшевик', 'mikrofilm': 'микрофильм', 'minonoses': 'миноносец',
                    'ofitsiant': 'официант', 'okkultizm': 'оккультизм', 'ordinares': 'ординарец',
                    'patsifist': 'пацифист', 'patsifizm': 'пацифизм', 'patsiyent': 'пациент', 'pestitsid': 'пестицид',
                    'platsdarm': 'плацдарм', 'platskart': 'плацкарт', 'plebissit': 'плебисцит',
                    'selluloid': 'целлулоид', 'siferblat': 'циферблат', 'sirkulyar': 'циркуляр',
                    'sitokimyo': 'цитокимё', 'sotsiolog': 'социолог', 'spetsifik': 'специфик', 'texnetsiy': 'технеций',
                    'ultimatum': 'ультиматум', 'umivalnik': 'умивальник', 'vermishel': 'вермишел[ь]',
                    'vestibyul': 'вестибюл[ь]', 'videofilm': 'видеофильм', 'aksioner': 'акционер',
                    'albatros': 'альбатрос', 'alpinist': 'альпинист', 'alpinizm': 'альпинизм', 'amalgama': 'амальгама',
                    'arergard': 'арьергард', 'banderol': 'бандерол[ь]', 'barelyef': 'барельеф', 'batalyon': 'батальон',
                    'batsilla': 'бацилла', 'belveder': 'бельведер', 'biofiltr': 'биофильтр', 'brakoner': 'браконьер',
                    'budilnik': 'будильник', 'buldenej': 'бульденеж', 'buldozer': 'бульдозер',
                    'diagonal': 'диагонал[ь]', 'dirijabl': 'дирижабл[ь]', 'dvigatel': 'двигател[ь]',
                    'emulsiya': 'эмульсия', 'endshpil': 'эндшпил[ь]', 'fagotsit': 'фагоцит', 'falsifik': 'фальсифик',
                    'feldsher': 'фельдшер', 'festival': 'фестивал[ь]', 'fitonsid': 'фитонцид', 'gaubitsa': 'гаубица',
                    'genotsid': 'геноцид', 'giatsint': 'гиацинт', 'gospital': 'госпитал[ь]', 'intervyu': 'интервью',
                    'inventar': 'инвентар[ь]', 'kalendar': 'календар[ь]', 'kalkulya': 'калькуля',
                    'kastryul': 'кастрюл[ь]', 'kinofilm': 'кинофильм', 'konsentr': 'концентр', 'konsulta': 'консульта',
                    'konveyer': 'конвейер', 'marganes': 'марганец', 'matritsa': 'матрица', 'medalyon': 'медальон',
                    'modelyer': 'модельер', 'monastir': 'монастир[ь]', 'nimpalto': 'нимпальто',
                    'parallel': 'параллел[ь]', 'pavilyon': 'павильон', 'pechenye': 'печенье', 'petlitsa': 'петлица',
                    'poyabzal': 'пойабзал', 'poyafzal': 'пойафзал', 'poyandoz': 'пойандоз', 'poyustun': 'пойустун',
                    'protsent': 'процент', 'protsess': 'процесс', 'rentabel': 'рентабел[ь]', 'retsidiv': 'рецидив',
                    'revolver': 'револьвер', 'rubilnik': 'рубильник', 'sekretar': 'секретар[ь]',
                    'selderey': 'сельдерей', 'sellofan': 'целлофан', 'sentyabr': 'сентябр[ь]', 'shifoner': 'шифоньер',
                    'shnitsel': 'шницел[ь]', 'shpindel': 'шпиндел[ь]', 'shtempel': 'штемпел[ь]',
                    'shtepsel': 'штепсел[ь]', 'shveysar': 'швейцар', 'silitsiy': 'силиций', 'sisterna': 'цистерна',
                    'spektakl': 'спектакл[ь]', 'ssenariy': 'сценарий', 'stronsiy': 'стронций', 'tablitsa': 'таблица',
                    'telefilm': 'телефильм', 'teplitsa': 'теплица', 'vedomost': 'ведомост[ь]', 'abssess': 'абсцесс',
                    'akletel': 'акварел[ь]', 'alkogol': 'алкогол[ь]', 'ansambl': 'ансамбл[ь]', 'apelsin': 'апельсин',
                    'atseton': 'ацетон', 'beletaj': 'бельэтаж', 'belgiya': 'бельгия', 'belting': 'бельтинг',
                    'bilyard': 'бильярд', 'bolonya': 'болонья', 'botsman': 'боцман', 'diafilm': 'диафильм',
                    'dotsent': 'доцент', 'ensefal': 'энцефал', 'esmines': 'эсминец', 'feleton': 'фельетон',
                    'folklor': 'фольклор', 'fransuz': 'француз', 'gastrol': 'гастрол[ь]', 'gelmint': 'гельминт',
                    'gorelef': 'горельеф', 'interer': 'интерьер', 'italyan': 'итальян', 'jenshen': 'женьшен[ь]',
                    'kanifol': 'канифол[ь]', 'kansler': 'канцлер', 'kapsyul': 'капсюл[ь]', 'karamel': 'карамел[ь]',
                    'kartech': 'картеч[ь]', 'karusel': 'карусел[ь]', 'kokteyl': 'коктейл[ь]', 'konsern': 'концерн',
                    'konsert': 'концерт', 'kontrol': 'контрол[ь]', 'konyunktura': 'конъюнктура',
                    'konyuktivit': 'коньюктивит', 'kulmina': 'кульмина', 'kultiva': 'культива', 'lotsman': 'лоцман',
                    'mayonez': 'майонез', 'melxior': 'мельхиор', 'molbert': 'мольберт', 'ofitser': 'офицер',
                    'oktyabr': 'октябр[ь]', 'partyer': 'партьер', 'penalti': 'пенальти', 'plastir': 'пластир[ь]',
                    'porshen': 'поршен[ь]', 'portfel': 'портфел[ь]', 'premyer': 'премьер', 'pristan': 'пристан[ь]',
                    'pritsep': 'прицеп', 'razyezd': 'разъезд', 'retsept': 'рецепт', 'sentner': 'центнер',
                    'senzura': 'цензура', 'sesarka': 'цесарка', 'seytnot': 'цейтнот', 'shagren': 'шагрен[ь]',
                    'shampun': 'шампун[ь]', 'shpatel': 'шпател[ь]', 'shpilka': 'шпилька', 'shtapel': 'штапел[ь]',
                    'silindr': 'цилиндр', 'sitoliz': 'цитолиз', 'skalpel': 'скальпел[ь]', 'sterjen': 'стержен[ь]',
                    'subyekt': 'субъект', 'tekstil': 'текстил[ь]', 'vaksina': 'вакцина', 'letyete': 'варьете',
                    'vernyer': 'верньер', 'vinetka': 'виньетка', 'vodevil': 'водевил[ь]', 'volfram': 'вольфрам',
                    'xrustal': 'хрустал[ь]', 'aksent': 'акцент', 'aksiya': 'акция', 'alyans': 'альянс',
                    'artikl': 'артикл[ь]', 'asfalt': 'асфальт', 'atelye': 'ателье', 'balneo': 'бальнео',
                    'balzam': 'бальзам', 'baryer': 'барьер', 'barrel': 'баррел[ь]', 'bazalt': 'базальт',
                    'binokl': 'бинокл[ь]', 'buldog': 'бульдог', 'bulyon': 'бульон', 'bullet': 'бульвар',
                    'chizel': 'чизел[ь]', 'dalton': 'дальтон', 'dekabr': 'декабр[ь]', 'delfin': 'дельфин',
                    'fakult': 'факульт', 'fevral': 'феврал[ь]', 'galvan': 'гальван', 'gantel': 'гантел[ь]',
                    'garmon': 'гармон[ь]', 'gersog': 'герцог', 'grifel': 'грифел[ь]', 'impuls': 'импульс',
                    'insult': 'инсульт', 'kalsiy': 'кальций', 'karate': 'каратэ', 'karyer': 'карьер',
                    'kartel': 'картел[ь]', 'kobalt': 'кобальт', 'konyak': 'коньяк', 'krovat': 'кроват[ь]',
                    'kuryer': 'курьер', 'lanset': 'ланцет', 'litsey': 'лицей', 'losyon': 'лосьон',
                    'migren': 'мигрен[ь]', 'moyupa': 'мойупа', 'nippel': 'ниппел[ь]', 'noyabr': 'ноябр[ь]',
                    'oblast': 'област[ь]', 'obyekt': 'объект', 'patrul': 'патрул[ь]', 'pechat': 'печат[ь]',
                    'pinset': 'пинцет', 'pitssa': 'пицца', 'pleyer': 'плейер', 'povest': 'повест[ь]',
                    'profil': 'профил[ь]', 'pulpit': 'пульпит', 'rantye': 'рантье', 'relyef': 'рельеф',
                    'retush': 'ретуш[ь]', 'ritsar': 'рицар[ь]', 'selsiy': 'цельсий', 'sement': 'цемент',
                    'senyor': 'сеньор', 'senzor': 'цензор', 'shinel': 'шинел[ь]', 'shpris': 'шприц',
                    'sirkul': 'циркул[ь]', 'sirroz': 'цирроз', 'sistit': 'цистит', 'sitata': 'цитата',
                    'sitrus': 'цитрус', 'slanes': 'сланец', 'slesar': 'слесар[ь]', 'spiral': 'спирал[ь]',
                    'statya': 'статья', 'stayer': 'стайер', 'stelka': 'стелька', 'sulfat': 'сульфат',
                    'sunami': 'цунами', 'syomka': 'съёмка', 'terset': 'терцет', 'tonnel': 'тоннел[ь]',
                    'tunnel': 'туннел[ь]', 'tyulen': 'тюлен[ь]', 'veksel': 'вексел[ь]', 'velvet': 'вельвет',
                    'ventil': 'вентил[ь]', 'vimpel': 'вимпел[ь]', 'volost': 'волост[ь]', 'vulgar': 'вульгар',
                    'yanvar': 'январ[ь]', 'yogurt': 'йогурт', 'abzas': 'абзац', 'aksiz': 'акциз', 'albom': 'альбом',
                    'aprel': 'апрел[ь]', 'artel': 'артел[ь]', 'delta': 'дельта', 'detal': 'детал[ь]',
                    'dizel': 'дизел[ь]', 'filtr': 'фильтр', 'folga': 'фольга', 'fonar': 'фонар[ь]', 'gavan': 'гаван[ь]',
                    'gilza': 'гильза', 'guash': 'гуаш[ь]', 'kabel': 'кабел[ь]', 'kafel': 'кафел[ь]', 'kalka': 'калька',
                    'kisel': 'кисел[ь]', 'kitel': 'кител[ь]', 'knyaz': 'княз[ь]', 'konki': 'коньки',
                    'kreml': 'кремл[ь]', 'klets': 'кварц', 'lager': 'лагер[ь]', 'latun': 'латун[ь]',
                    'losos': 'лосос[ь]', 'mayor': 'майор', 'mebel': 'мебел[ь]', 'medal': 'медал[ь]',
                    'model': 'модел[ь]', 'motel': 'мотел[ь]', 'multi': 'мульти', 'nenes': 'ненец', 'nikel': 'никел[ь]',
                    'palma': 'пальма', 'palto': 'пальто', 'panel': 'панел[ь]', 'parol': 'парол[ь]', 'pedal': 'педал[ь]',
                    'polka': 'полька', 'pulpa': 'пульпа', 'pyesa': 'пьеса', 'ranes': 'ранец', 'rayon': 'район',
                    'reket': 'рэкет', 'rezba': 'резьба', 'riyel': 'риел[ь]', 'royal': 'роял[ь]', 'saldo': 'сальдо',
                    'salto': 'сальто', 'sanga': 'цанга', 'sapfa': 'цапфа', 'sedra': 'цедра', 'seriy': 'церий',
                    'seziy': 'цезий', 'singa': 'цинга', 'sinka': 'синька', 'siren': 'сирен[ь]', 'sobol': 'собол[ь]',
                    'sokol': 'цокол[ь]', 'sudya': 'судья', 'syezd': 'съезд', 'tabel': 'табел[ь]', 'tigel': 'тигел[ь]',
                    'tokar': 'токар[ь]', 'ultra': 'ультра', 'vanil': 'ванил[ь]', 'yakor': 'якор[ь]', 'alfa': 'альфа',
                    'bron': 'брон[ь]', 'drel': 'дрел[ь]', 'duel': 'дуэл[ь]', 'emal': 'эмал[ь]', 'film': 'фильм',
                    'foye': 'фойе', 'fris': 'фриц', 'gers': 'герц', 'golf': 'гольф', 'iyul': 'июл[ь]', 'iyun': 'июн[ь]',
                    'kyat': 'кьят', 'neft': 'нефт[ь]', 'otel': 'отел[ь]', 'pech': 'печ[ь]', 'puls': 'пульс',
                    'pult': 'пульт', 'rels': 'рельс', 'rubl': 'рубл[ь]', 'seld': 'сельд[ь]', 'sent': 'цент',
                    'senz': 'ценз', 'sian': 'циан', 'sikl': 'цикл', 'sink': 'цинк', 'sirk': 'цирк', 'stil': 'стил[ь]',
                    'talk': 'тальк', 'tyul': 'тюл[ь]', 'util': 'утил[ь]', 'vals': 'вальс', 'verf': 'верф[ь]',
                    'volt': 'вольт', 'yoga': 'йога', 'yuan': 'юан[ь]', 'alt': 'альт', 'mil': 'мил[ь]', 'nol': 'нол[ь]',
                    'rol': 'рол[ь]', 'rul': 'рул[ь]', 'sex': 'цех', 'yana-da': 'янада'}
vovels = ["a", "o", "u", "а", "о", "у"]
vovels2 = ["a", "o", "u", "e", "i", "а", "о", "у", "е", "и"]
pre_retranslit = {'sirka': 'сирка', 'singari': 'сингари', 'prinsip': 'принцип', 'detsi': 'деци', 'sikl': 'цикл',
                  'vitse': 'вице', 'devalvatsiya': 'девальвация', 'valvatsiya': 'вальвация', 'pensiya': 'пенсия',
                  'versiya': 'версия', 'jinsiyat': 'жинсият', 'Sirka': 'Сирка', 'Singari': 'Сингари',
                  'Prinsip': 'Принцип', 'Detsi': 'Деци', 'Sikl': 'Цикл', 'Vitse': 'Вице', 'Devalvatsiya': 'Девальвация',
                  'Valvatsiya': 'Вальвация', 'Pensiya': 'Пенсия', 'Versiya': 'Версия', 'Jinsiyat': 'Жинсият',
                  'SIRKA': 'СИРКА', 'SINGARI': 'СИНГАРИ', 'PRINSIP': 'ПРИНЦИП', 'DETSI': 'ДЕЦИ', 'SIKL': 'ЦИКЛ',
                  'VITSE': 'ВИЦЕ', 'DEVALVATSIYA': 'ДЕВАЛЬВАЦИЯ', 'VALVATSIYA': 'ВАЛЬВАЦИЯ', 'PENSIYA': 'ПЕНСИЯ',
                  'VERSIYA': 'ВЕРСИЯ', 'JINSIYAT': 'ЖИНСИЯТ'}
post_retranslit = {'bsiya': 'бция', 'bsion': 'бцион', 'ksiya': 'кция', 'ksion': 'кцион', 'nsiya': 'нция',
                   'nsion': 'нцион', 'rsiya': 'рция', 'rsion': 'рцион', 'psiya': 'пция', 'psion': 'пцион',
                   'tsiya': 'ция', 'tsist': 'цист', 'tsizm': 'цизм', 'tsit': 'цит', 'tsevt': 'цевт', 'tsept': 'цепт',
                   'tser': 'цер', 'tsia': 'циа', 'sia': 'циа', 'tsikl': 'цикл', 'tsio': 'цио', 'tsiu': 'циу',
                   'siu': 'циу', 'BSIYA': 'БЦИЯ', 'BSION': 'БЦИОН', 'KSIYA': 'КЦИЯ', 'KSION': 'КЦИОН', 'NSIYA': 'НЦИЯ',
                   'NSION': 'НЦИОН', 'RSIYA': 'РЦИЯ', 'RSION': 'РЦИОН', 'PSIYA': 'ПЦИЯ', 'PSION': 'ПЦИОН',
                   'TSIYA': 'ЦИЯ', 'TSIST': 'ЦИСТ', 'TSIZM': 'ЦИЗМ', 'TSIT': 'ЦИТ', 'TSEVT': 'ЦЕВТ', 'TSEPT': 'ЦЕПТ',
                   'TSER': 'ЦЕР', 'TSIA': 'ЦИА', 'SIA': 'ЦИА', 'TSIKL': 'ЦИКЛ', 'TSIO': 'ЦИО', 'TSIU': 'ЦИУ',
                   'SIU': 'ЦИУ'}
l_letters_l2c = ["w", "W", "YO'", "Yo'", "yo'", "YO", "Yo", "yo", "YA", "Ya", "ya", "YE", "Ye", "ye", "YU", "Yu", "yu",
                 "CH", "Ch", "ch", "S'H", "S'h", "s'h", "SH", "Sh", "sh", "A", "a", "B", "b", "D", "d", "F", "f", "G",
                 "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q",
                 "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "X", "x", "Y", "y", "Z", "z", "c", "C"]
c_letters_l2c = ["в", "В", "ЙЎ", "Йў", "йў", "Ё", "Ё", "ё", "Я", "Я", "я", "Е", "Е", "е", "Ю", "Ю", "ю", "Ч", "Ч", "ч",
                 "СҲ", "Сҳ", "сҳ", "Ш", "Ш", "ш", "А", "а", "Б", "б", "Д", "д", "Ф", "ф", "Г", "г", "Ҳ", "ҳ", "И", "и",
                 "Ж", "ж", "К", "к", "Л", "л", "М", "м", "Н", "н", "О", "о", "П", "п", "Қ", "қ", "Р", "р", "С", "с",
                 "Т", "т", "У", "у", "В", "в", "Х", "х", "Й", "й", "З", "з", "с", "С"]
c_letters_c2l = ["ы", "Ы", "ЕЪ", "Еъ", "еъ", "СҲ", "Сҳ", "сҳ", "ЪЮ", "ъю", "ЬЮ", "ью", "ЬО", "ьо", "ЬЕ", "ье", "ЬЁ",
                 "ьё", "ЪЕ", "ъе", "ЪЁ", "ъё", "А", "а", "Б", "б", "В", "в", "Г", "г", "Д", "д", "ё", "Ж", "ж", "З",
                 "з", "И", "и", "Й", "й", "К", "к", "Л", "л", "М", "м", "Н", "н", "О", "о", "П", "п", "Р", "р", "С",
                 "с", "Т", "т", "У", "у", "Ф", "ф", "Х", "х", "ч", "ш", "Э", "э", "ю", "я", "Ў", "ў", "Қ", "қ", "Ғ",
                 "ғ", "Ҳ", "ҳ", "Ъ", "ъ", "Ь", "ь"]
l_letters_c2l = ["i", "I", "Eʼ", "Eʼ", "eʼ", "SʼH", "Sʼh", "sʼh", "YU", "yu", "YU", "yu", "YO", "yo", "YE", "ye", "YO",
                 "yo", "YE", "ye", "YO", "yo", "A", "a", "B", "b", "V", "v", "G", "g", "D", "d", "yo", "J", "j", "Z",
                 "z", "I", "i", "Y", "y", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "R", "r", "S",
                 "s", "T", "t", "U", "u", "F", "f", "X", "x", "ch", "sh", "E", "e", "yu", "ya", "Oʻ", "oʻ", "Q", "q",
                 "Gʻ", "gʻ", "H", "h", "ʼ", "ʼ", "", ""]
word_head = ["aʼ", "ab", "ac", "ad", "ae", "af", "ag", "ah", "aj", "ak", "al", "am", "an", "ao", "ap", "aq", "ar", "as",
             "at", "au", "av", "ax", "ay", "az", "ba", "be", "bi", "bl", "bo", "br", "bu", "by", "ch", "da", "de", "di",
             "do", "dr", "du", "dv", "eʼ", "eb", "ec", "ed", "ef", "eg", "eh", "ek", "el", "em", "en", "ep", "er", "es",
             "et", "ev", "ey", "ez", "fa", "fe", "fi", "fl", "fo", "fr", "ft", "fu", "gʻ", "ga", "ge", "gi", "gl", "gn",
             "go", "gr", "gu", "gv", "ha", "he", "hi", "ho", "hu", "ib", "ic", "id", "if", "ig", "ih", "ij", "ik", "il",
             "im", "in", "io", "ip", "iq", "ir", "is", "it", "iv", "ix", "iy", "iz", "ja", "je", "ji", "jo", "ju", "jy",
             "ka", "ke", "ki", "kl", "kn", "ko", "kr", "ks", "ku", "kv", "la", "le", "li", "lo", "lu", "ly", "ma", "mb",
             "me", "mi", "mo", "mu", "my", "na", "ne", "ni", "nj", "no", "nu", "ny", "oʻ", "ob", "oc", "od", "of", "og",
             "oh", "oi", "oj", "ok", "ol", "om", "on", "op", "oq", "or", "os", "ot", "ov", "ox", "oy", "oz", "pa", "pe",
             "pi", "pl", "pn", "po", "pr", "ps", "pu", "px", "py", "qa", "qe", "qi", "qo", "qu", "ra", "re", "ri", "ro",
             "ru", "ry", "sa", "se", "sf", "sh", "si", "sk", "sl", "sm", "sn", "so", "sp", "ss", "st", "su", "sv", "sx",
             "sy", "ta", "tb", "te", "ti", "to", "tr", "tu", "tv", "tx", "ty", "ua", "ub", "uc", "ud", "uf", "ug", "uh",
             "uk", "ul", "um", "un", "up", "uq", "ur", "us", "ut", "uv", "ux", "uy", "uz", "va", "ve", "vi", "vo", "vr",
             "vu", "vy", "vz", "xa", "xe", "xi", "xl", "xm", "xo", "xr", "xu", "ya", "ye", "yi", "yo", "yu", "za", "ze",
             "zi", "zo", "zu"]
tail_names = {"-a": ["-a", "Hayrat yuklamasi"], "-chi": ["-chi", "Soʻroq yuklamasi"],
              "-da": ["-da", "Taʼkid yuklamasi"], "-ku": ["-ku", "Soʻroq yuklamasi"], "-u": ["-u", "Zidlash yuklamasi"],
              "-ya": ["-ya", "Hayrat yuklamasi"], "-yu": ["-yu", "Zidlash yuYuklamasi"], "a": ["a", "Kelgusi zamon"],
              "u": ["u", "Kelgusi zamon (k.)"], "b": ["b", "Ravishdosh"], "cha": ["cha", "Qiyoslash"],
              "chalik": ["chalik", "Chegara"], "da": ["da", "Oʻrin-payt"], "dagi": ["dagi", "Joylashuv"],
              "dan": ["dan", "Chiqish"], "day": ["day", "Oʻxshatish"], "dek": ["dek", "Oʻxshatish"],
              "deg": ["dek", "Oʻxshatish"], "di": ["di", "Oʻtgan zamon"], "digan": ["digan", "Sifatdosh"],
              "dir": ["dir", "Urgʻu yuklamasi"], "dur": ["dur", "Urgʻu yuklamasi (k.)"], "ga": ["ga", "Joʻnalish"],
              "gach": ["gach", "Tugallanish"], "gacha": ["gacha", "Muddat"], "gan": ["gan", "Sifatdosh"],
              "gay": ["gay", "Kelgusi zamon (k.)"], "gi": ["gi", "Istak mayli"], "gin": ["gin", "Buyruq mayli"],
              "gina": ["gina", "Ayirish / erkalash"], "gu": ["gu", "Qiyoslash"], "gun": ["gun", "Muddat"],
              "gur": ["gur", "Tilak mayli"], "guvchi": ["guvchi", "Sifatdosh"], "i": ["i", "3-sh. birlik"],
              "ib": ["ib", "Ravishdosh"], "im": ["im", "1-sh. birlik"], "imiz": ["imiz", "1-sh. koʻplik"],
              "in": ["in", "Kuchaytirish (k.)"], "ing": ["ing", "2-sh. birlik"], "ingiz": ["ingiz", "2-sh. koʻplik"],
              "ish": ["ish", "Harakat nomi"], "jak": ["jak", "Kelgusi zamon (k.)"],
              "jag": ["jak", "Kelgusi zamon (k.)"], "k": ["k", "1-sh. koʻplik"], "g": ["k", "1-sh. koʻplik"],
              "kan": ["kan", "[ekan]"], "ki": ["ki", "Taʼkid yuklamasi"],
              "lar": ["lar", "Koʻplik / hurmat / mubolagʻa"], "lik": ["lik", "Mavhumlik"], "lig": ["lik", "Mavhumlik"],
              "m": ["m", "1-sh. birlik"], "ma": ["ma", "Inkor shakl"], "man": ["man", "1-sh. birlik kesim"],
              "mas": ["mas", "Inkor shakl"], "mi": ["mi", "Soʻroq yuklamasi"], "mish": ["mish", "Taxmin yuklamasi"],
              "miz": ["miz", "1-sh. koʻplik kesim"], "moq": ["moq", "Harakat nomi"], "mogʻ": ["moq", "Harakat nomi"],
              "moqchi": ["moqchi", "Maqsad mayli"], "moqda": ["moqda", "Hozirgi zamon (k.)"],
              "ng": ["ng", "2-sh. birlik"], "ngiz": ["ngiz", "2-sh. koʻplik"], "ni": ["ni", "Tushum"],
              "niki": ["niki", "Tegishlilik"], "ning": ["ning", "Qaratqich"], "ol": ["ol", "[olmoq]"],
              "oq": ["oq", "Darhollik yuklamasi"], "ov": ["ov", "Gumon yuklamasi"], "qol": ["qol", "[qolmoq]"],
              "r": ["r", "Kelgusi zamon gumon"], "roq": ["roq", "Qiyosiy daraja"], "rogʻ": ["roq", "Qiyosiy daraja"],
              "s": ["s", "Ravishdosh (inkor)"], "sa": ["sa", "Shart mayli"], "san": ["san", "2-sh. birlik kesim"],
              "si": ["si", "3-sh. birlik"], "sin": ["sin", "Buyruq mayli"],
              "siz": ["siz", "2-sh. koʻplik kesim / mahrumlik"], "ti": ["ti", "[yapti]"], "uv": ["uv", "Harakat nomi"],
              "uvchi": ["uvchi", "Sifatdosh"], "ver": ["ver", "[bermoq]"], "y": ["y", "Kelgusi zamon"],
              "yap": ["yap", "Hozirgi zamon"], "yoq": ["yoq", "Darhollik yuklamasi"], "yot": ["yot", "Davomiylik"],
              "yotib": ["yotib", "Ravishdosh"], "yotir": ["yotir", "Davomiylik (k.)"],
              "yov": ["yov", "Gumon yuklamasi"]}
speech_parts = {"at": "atoqli ot", "is": "ism", "sh": "sharif", "tn": "toponim", "ot": "ot", "sf": "sifat",
                "rv": "ravish", "ol": "olmosh", "sn": "son", "fl": "feʼl", "ys": "yordamchi soʻz"}
complex_words = ["aʼzoyi badan", "achom qil", "adoyi tamom", "ahd-u paymon", "ak-ak qil", "ak-ak qilish",
                 "alayhi vasallam", "amerika qoʻshma shtatlari", "andarmon boʻl", "andarmon boʻlish",
                 "antigua va barbuda", "ar-ar terak", "assalomu alaykum", "baham koʻr", "baham koʻril", "baham koʻrish",
                 "baholi qudrat", "baloyi azim", "baloyi battar", "baloyi nafs", "baloyi nogahon", "baloyi qazo",
                 "baloyi xudo", "bardor-bardor qil", "bardor-bardor qildir", "bardor-bardor qilin",
                 "bardor-bardor qilish", "barham ber", "barham beril", "barham berish", "barham top", "barham ye",
                 "barpo boʻl", "barpo boʻlish", "barpo et", "barpo etil", "barpo etish", "barpo ettir", "barpo ettiril",
                 "barpo ettirish", "barpo qil", "barpo qildir", "barpo qildiril", "barpo qildirish", "barpo qilin",
                 "barpo qilish", "bazmi jamshid", "bekam-u koʻst", "bekordan bekorga", "benom-u nishon",
                 "bermud orollari", "bez-bez ogʻri", "bez-bez qil", "binoan alayh", "bir-u bor",
                 "birlashgan arab amirliklari", "birlashgan qirollik", "bitta-yu bitta", "bogʻ-u boʻston", "bol-u par",
                 "bosniya va gersegovina", "bud-u shud", "burkina faso", "buyuk britaniya", "dardi bedavo",
                 "dimogʻ-firoq qil", "dimogʻ-firoq qilish", "diydayi giryon", "dogʻ-dogʻ oʻrta", "dogʻ-dogʻ oʻrtan",
                 "dominika respublikasi", "duoyi bad", "duoyi jon", "duoyi xayr", "ekvatorli gvineya", "el salvador",
                 "enka-tinkasini chiqair", "enka-tinkasini chiqairsh", "enka-tinkasini qurit",
                 "enka-tinkasini quritish", "epaqaga kel", "epaqaga keltir", "epaqaga keltiril", "epaqaga keltirish",
                 "epaqaga ol", "epaqaga oldir", "epaqaga oldiril", "epaqaga oldirish", "epaqaga olin", "epaqaga olish",
                 "epaqaga sol", "epaqaga soldir", "epaqaga soldiril", "epaqaga soldirish", "epaqaga solin",
                 "epaqaga solish", "epaqaga tush", "epaqaga tushir", "epaqaga tushiril", "epaqaga tushirish",
                 "epaqaga tushish", "fath-u nusrat", "fikr-u mulohaza", "fikr-u xayol", "fil suyak sohili",
                 "gʻarra-sharra sarf qil", "gʻarra-sharra sarf qilin", "gʻarra-sharra sarf qilish", "gʻingʻ-gʻingʻ qil",
                 "gʻingʻ-gʻingʻ qildir", "gʻingʻ-gʻingʻ qildirish", "gʻingʻ-gʻingʻ qilish", "gʻingʻir-gʻingʻir qil",
                 "gʻingʻir-gʻingʻir qilish", "gʻippa boʻgʻ", "gʻippa boʻgʻil", "gʻippa boʻgʻish", "gʻiring de",
                 "gʻiring degiz", "gʻiring deyil", "gʻiring deyish", "gar-gar kekir", "gar-gar kekirish",
                 "gard-gard qil", "giryona boʻl", "giryona boʻlish", "harb-u zarb", "hash-pash deguncha",
                 "hoʻl-u quruq", "ilm-u amal", "ilm-u fan", "ilm-u maʼrifat", "jang-u jadal",
                 "janubiy afrika respublikasi", "janubiy amerika", "janubiy koreya", "janubiy sudan",
                 "javdir-javdir boq", "javdir-javdir boqish", "javdir-javdir qara", "javdir-javdir qarash", "jon-u dil",
                 "jon-u jahon", "jon-u tan", "kabo verde", "koʻz-koʻz qil", "koʻz-koʻz qildir", "koʻz-koʻz qildiril",
                 "koʻz-koʻz qildirish", "koʻz-koʻz qilin", "koʻz-koʻz qilish", "koʻz-quloq boʻl", "koʻz-quloq boʻlin",
                 "koʻz-quloq boʻlish", "kongo demokratik respublikasi", "kongo respublikasi", "kosta rika",
                 "kvadrat-uyalab ek", "kvadrat-uyalab ekil", "kvadrat-uyalab ekish", "kvadrat-uyalab ektir",
                 "kvadrat-uyalab ektiril", "kvadrat-uyalab ektirish", "lof-qof ur", "lof-qof urish", "mahv boʻl",
                 "mahv boʻlish", "mahv et", "mahv etil", "mahv etish", "mahv qil", "mahv qilin", "mahv qilish",
                 "markaziy afrika respublikasi", "marshall orollari", "mikroneziya federativ shtatlari", "mol-u dunyo",
                 "mol-u manol", "murosa-yu madora", "muvaffaq boʻl", "muvaffaq boʻlin", "muvaffaq boʻlish",
                 "muyassar boʻl", "muyassar boʻlin", "muyassar boʻlish", "nasl-u nasab", "nazar-pisand qil",
                 "nazar-pisand qilish", "neleta-yu cheleta", "noʻsh ayla", "noʻsh aylan", "noʻsh aylat", "noʻsh piyoz",
                 "noz-u karashma", "noz-u neʼmat", "nuqtayi nazar", "oʻlib-netib qol", "oʻlib-netib qolish",
                 "oʻng-u soʻl", "oʻng-u ters", "oh-u zor", "oldi-ortiga qaramay", "olma-kesak ter", "oppon-soppon boʻl",
                 "oppon-soppon boʻlish", "ozor-bezor boʻl", "ozor-bezor boʻlish", "padari buzrukvor", "pand ber",
                 "pand beril", "pand ye", "pand yeyish", "papua yangi gvineya", "peshvoz chiq", "peshvoz chiqil",
                 "peshvoz chiqish", "peshvoz tur", "peshvoz turil", "peshvoz turish", "peshvoz yur", "peshvoz yuril",
                 "peshvoz yurish", "poy-chogʻ ol", "poy-chogʻ olish", "qisti-bastiga ol", "qisti-bastiga olish",
                 "quling oʻrgilsin", "quti loyamut", "rasvoyi olam", "rizqi roʻz", "rozi dil", "ruju qil", "ruju qilin",
                 "ruju qilish", "ruju qoʻy", "ruju qoʻyil", "ruju qoʻyish", "sadqayi sar", "sahv-u xato", "san marino",
                 "san-manga bor", "san-manga borish", "san-tome va prinsipi", "sarak-sarak qil", "sarak-sarak qilish",
                 "saudiya arabistoni", "sayr-u sayohat", "sayr-u tomosha", "sehr-u jodu", "sen-menga bor",
                 "sen-menga borish", "sent vinsent va grenadinlar", "seyshell orollari", "shab-u roʻz", "sharqiy timor",
                 "shimoliy amerika", "shimoliy koreya", "shol-shol boʻl", "shol-shol boʻlish", "solomon orollari",
                 "syerra leone", "taʼsis et", "taʼsis etil", "taʼsis etish", "taʼsis ettir", "taʼsis ettiril",
                 "taʼsis ettirish", "taʼsis qil", "taʼsis qildir", "taʼsis qildiril", "taʼsis qildirish",
                 "taʼsis qilin", "taʼsis qilish", "taka-taka qil", "taka-taka qilish", "tap tort", "tarjimayi hol",
                 "teng-u tush", "teta-poya boʻl", "teta-poya boʻlish", "teta-poya qil", "teta-poya qilish",
                 "tit-pit boʻl", "tit-pit qil", "tit-pit qilin", "tit-pit qilish", "tit-pitini chiqar",
                 "tit-pitini chiqarish", "togʻ-u tosh", "toj-u taxt", "trinidad va tobago", "tun-u kun",
                 "va alaykum assalom", "vallis va futuna", "vaqti-vaqti bilan", "vayron-talqon qil",
                 "vayron-talqon qilin", "vayron-talqon qilish", "voyaga yet", "voyaga yetish", "voyaga yetkaz",
                 "voyaga yetkazil", "voyaga yetkazish", "voz kech", "voz kechdir", "voz kechdiril", "voz kechdirish",
                 "voz kechil", "voz kechish", "xesh-u aqrabo", "xitoy xalq respublikasi", "xor-u xas", "xor-u zor",
                 "yangi zelandiya", "yasan-tusan qil", "yasan-tusan qilish", "yebir-yesir qil", "yebir-yesir qilin",
                 "yebir-yesir qilish", "yer bagʻirlab", "yosh-u qari", "yumma-yumma yigʻla", "yumma-yumma yigʻlash",
                 "yumma-yumma yigʻlat", "zikr-u samo", "zoʻrma-zoʻrakilik bilan", "zudlik bilan", "ilmiy-tadqiqot",
                 "ilmiy-ishlab chiqarish", "oʻmbaloq osh", "oʻmbaloq oshish", "oʻmbaloq oshir", "oʻmbaloq oshiril",
                 "oʻmbaloq oshirish", "oʻmbaloq oshil", "ish haqi", "yoʻl haqi", "qoʻl haqi", "ustama haqi",
                 "qalam haqi", "xizmat haqi", "ijara haqi", "kira haqi"]


def replace_array(text, a1, a2):
    for i, item in enumerate(a1):
        text = re.sub(item, a2[i], text)
    return text


def replace_parts(text, a):
    for key in a:
        text = re.sub(key, a[key], text)
    return text


# function replaceWordsL2C(text, a) {
#   for (let key in a) {
#     let replacement = a[key];
#     let wrapped = "\\b" + key;
#     let pat = new RegExp(wrapped,"gi");
#     text = text.replace(pat, function(match) {
#       if (match == match.toLowerCase()) {
#         return replacement;
#       } else if (match == match.toUpperCase()) {
#         return replacement.toUpperCase();
#       } else {
#         return replacement.charAt(0).toUpperCase() + replacement.slice(1);
#       }
#     });
#   }
#   return text;
# }

def replace_words_l2c(text, a):
    for key in a:
        replacement = a[key]
        wrapped = "\\b" + key
        # while re.match(wrapped, replacement, text):
        text = re.sub(wrapped, replacement, text)
    return text


def translate_to_cyrillic(text):
    text = re.sub("Gʻ|Gʼ|G’|G'|G`|G‘", "Ғ", text)
    text = re.sub("gʻ|gʼ|g’|g'|g`|g‘", "ғ", text)
    text = re.sub("Oʻ|Oʼ|O’|O'|O`|O‘", "Ў", text)
    text = re.sub("oʻ|oʼ|o’|o'|o`|o‘", "ў", text)
    text = re.sub("ʻ|’|'|`|‘", "ʼ", text)
    text = re.sub("\\bMЎJ", "МЎЪЖ", text)
    text = re.sub("\\bMўj", "Мўъж", text)
    text = re.sub("\\bmўj", "мўъж", text)
    text = re.sub("\\bMЎT", "МЎЪТ", text)
    text = re.sub("\\bMўt", "Мўът", text)
    text = re.sub("\\bmўt", "мўът", text)
    text = re.sub("“([^“”]+)”", '«\\1»', text)
    text = re.sub("([^\"]+)", '«\\1»', text)
    text = re.sub("-da\\b", "dа", text)
    text = re.sub("-ku\\b", "ku", text)
    text = re.sub("-chi\\b", "chi", text)
    text = re.sub("-yu\\b", "yu", text)
    text = re.sub("-u\\b", "u", text)
    text = replace_parts(text, pre_retranslit)
    text = replace_words_l2c(text, retranslit_words)
    text = replace_parts(text, post_retranslit)
    text = re.sub("ʼ([A-Z])", "Ъ\\1", text)
    text = re.sub("ʼ([a-z])", "ъ\\1", text)
    text = re.sub("([ОЕOE])ʼ", "\\1Ъ", text)
    text = re.sub("([оеoe])ʼ", "\\1ъ", text)
    text = replace_array(text, l_letters_l2c, c_letters_l2c)
    text = re.sub("\\[ь\\]([a-zа-яўқғҳ])", "\\1", text)
    text = re.sub("\\[Ь\\]([A-ZА-ЯЎҚҒҲ])", "\\1", text)
    text = re.sub("\\[ь\\]([^\\w])|\\[ь\\]$", "ь\\1", text)
    text = re.sub("\\[Ь\\]([^\\w])|\\[Ь\\]$", "Ь\\1", text)
    text = re.sub("^E|([^БВГДЕЁЖЗИЙКЛМНПРСТФХЦЧШЪЫЬЭЮЯЎҚҒҲбвгдеёжзийклмнпрстфхцчшъыьэюяўқғҳ])E|([\\s+])E",
                  "\\1\\2Э", text)
    text = re.sub("^e|([^БВГДЕЁЖЗИЙКЛМНПРСТФХЦЧШЪЫЬЭЮЯЎҚҒҲбвгдеёжзийклмнпрстфхцчшъыьэюяўқғҳ])e|([\\s+])e",
                  "\\1\\2э", text)
    text = re.sub("e", "е", text)
    text = re.sub("([аоу])эв", "\\1ев", text)
    text = re.sub("([АаОоУу])ЭВ", "\\1ЕВ", text)
    text = re.sub("(\\d+)-(январ|феврал|март|апрел|май|июн|июл|август|сентябр|октябр|ноябр|декабр"
                  + "|ЯНВАР|ФЕВРАЛ|МАРТ|АПРЕЛ|МАЙ|ИЮН|ИЮЛ|АВГУСТ|СЕНТЯБР|ОКТЯБР|НОЯБР|ДЕКАБР)", "\\1 \\2", text)
    text = re.sub("(\\d+)-(йил|ЙИЛ|й\\.)", "\\1 \\2", text)
    text = re.sub("([^БВГДЕЁЖЗИЙКЛМНПРСТФХЦЧШЪЫЬЭЮЯЎҚҒҲбвгдеёжзийклмнпрстфхцчшъыьэюяўқғҳ])"
                  + "Яна-да([^БВГДЕЁЖЗИЙКЛМНПРСТФХЦЧШЪЫЬЭЮЯЎҚҒҲбвгдеёжзийклмнпрстфхцчшъыьэюяўқғҳ])",
                  "\\1Янада\\2", text)
    text = re.sub("([^БВГДЕЁЖЗИЙКЛМНПРСТФХЦЧШЪЫЬЭЮЯЎҚҒҲбвгдеёжзийклмнпрстфхцчшъыьэюяўқғҳ])яна-да(["
                  "^БВГДЕЁЖЗИЙКЛМНПРСТФХЦЧШЪЫЬЭЮЯЎҚҒҲбвгдеёжзийклмнпрстфхцчшъыьэюяўқғҳ])", "\\1янада\\2", text)
    return text


def translate_to_latin(text):
    text = re.sub("\"([^\"]+)\"", '"\\1"', text)
    text = re.sub("«([^»]+)»", '"\\1"', text)
    text = replace_array(text, c_letters_c2l, l_letters_c2l)
    text = re.sub("([A-Z])Ё|Ё([A-Z])", "\\1YO\\2", text)
    text = re.sub("Ё([a-z])|Ё(\\s+)|Ё", "Yo\\1\\2", text)
    text = re.sub("([A-Z])Ч|Ч([A-Z])", "\\1CH\\2", text)
    text = re.sub("Ч([a-z])|Ч(\\s+)|Ч", "Ch\\1\\2", text)
    text = re.sub("([A-Z])Ш|Ш([A-Z])", "\\1SH\\2", text)
    text = re.sub("Ш([a-z])|Ш(\\s+)|Ш", "Sh\\1\\2", text)
    text = re.sub("([A-Z])Ю|Ю([A-Z])", "\\1YU\\2", text)
    text = re.sub("Ю([a-z])|Ю(\\s+)|Ю", "Yu\\1\\2", text)
    text = re.sub("([A-Z])Я|Я([A-Z])", "\\1YA\\2", text)
    text = re.sub("Я([a-z])|Я(\\s+)|Я", "Ya\\1\\2", text)
    text = re.sub("([AOUЕI])Ц([AOUЕI])", "\\1TS\\2", text)
    text = re.sub("([aouеi])ц([aouеi])", "\\1ts\\2", text)
    text = re.sub("Ц", "S", text)
    text = re.sub("ц", "s", text)
    text = re.sub("([^\\w])Е([A-Z])|([AOUEI])Е([A-Z])|^Е([A-Z])", "\\1\\3YE\\2\\4\\5", text)
    text = re.sub("([^\\w])Е([a-z])|([^\\w])Е([^\\w])|^Е([a-z])|^Е([^\\w])'|([^\\w])Е", "\\1\\3\\7Ye\\2\\4\\5\\6", text)
    text = re.sub("Е", "E", text)
    text = re.sub("^е|([^\\w])е|([aouei])е", "\\1\\2ye", text)
    text = re.sub("е", "e", text)
    text = re.sub("[ʻ’'`‘]+", "‘", text)
    text = re.sub("ʻʼ", "ʻ", text)
    text = re.sub("‘ʼ", "ʻ", text)
    text = re.sub("(\\d+)\\s+(yanvar|fevral|mart|aprel|may|iyun|iyul|avgust|sentyabr|oktyabr|noyabr|dekabr|"
                  + "YANVAR|FEVRAL|MART|APREL|MAY|IYUN|IYUL|AVGUST|SENTYABR|OKTYABR|NOYABR|DEKABR)",
                  "\\1-\\2", text)
    text = re.sub("(\\d{3,4})\\s+(yil|YIL|y\\.)", "\\1-\\2", text)
    text = re.sub("\\bnuqtai nazar", "nuqtayi nazar", text)
    text = re.sub("\\btarjimai hol", "tarjimayi hol", text)
    text = re.sub("\\byanada\\b", "yana-da", text)

    return text
