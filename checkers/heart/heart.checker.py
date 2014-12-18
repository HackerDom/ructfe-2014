#!/usr/bin/python3

import uuid
import random
import string
import requests as r

from httpchecker import *

GET = 'GET'
POST = 'POST'
PORT = 80

class Checker(HttpCheckerBase):
	def session(self, addr):
		s = r.Session()
		ua = self.randua()
		s.headers['User-Agent'] = ua[0]
		s.headers['Accept'] = '*/*'
		s.headers['Accept-Language'] = 'en-US,en;q=0.5'
		return s

	def url(self, addr, suffix):
		return 'http://{}:{}{}'.format(addr, PORT, suffix)

	def parseresponse(self, response, path):
		try:
			if response.status_code != 200:
				raise HttpWebException(response.status_code, path)
			try:
				result = response.json()
				#self.debug(result)
				return result
			except ValueError:
				raise r.exceptions.HTTPError('failed to parse response')
		finally:
			response.close()

	def parsestringresponse(self, response, path):
		try:
			if response.status_code != 200:
				raise HttpWebException(response.status_code, path)
			result = response.text
			return result
		finally:
			response.close()

	def jpost(self, s, addr, suffix, data = None):
		response = s.post(self.url(addr, suffix), data, timeout=5)
		return self.parseresponse(response, suffix)

	def spost(self, s, addr, suffix, data = None):
		response = s.post(self.url(addr, suffix), data, timeout=5)
		return self.parsestringresponse(response, suffix)

	def jget(self, s, addr, suffix):
		response = s.get(self.url(addr, suffix), timeout=5)
		return self.parseresponse(response, suffix)

	def sget(self, s, addr, suffix):
		response = s.get(self.url(addr, suffix), timeout=5)
		return self.parsestringresponse(response, suffix)

	def randword(self):
		word = ''
		rnd = random.randrange(2,10)
		for i in range(rnd):
			word += random.choice(string.ascii_lowercase)
		return word

	def randphrase(self):
		phrase = ''
		rnd = random.randrange(1,4)
		for i in range(rnd):
			phrase += ' ' + self.randword();
		return phrase.lstrip()

	def check(self, addr):
		s = self.session(addr)

		result = self.sget(s, addr, '/')
		if not result or len(result) == 0:
			print('get / failed')
			return EXITCODE_MUMBLE

		return EXITCODE_OK

	def randua(self):
		return random.choice([
			['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'],
			['Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36'],
			['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'],
			['Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'],
			['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'],

			['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 YaBrowser/14.8.1985.11875 Safari/537.36'],
			['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 YaBrowser/14.8.1985.12017 Safari/537.36'],
			['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 YaBrowser/14.8.1985.12018 Safari/537.36'],
			['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 YaBrowser/14.8.1985.12084 Safari/537.36'],
			['Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 YaBrowser/14.8.1985.12084 Safari/537.36'],

			['Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/33.0.1750.152 Chrome/33.0.1750.152 Safari/537.36'],
			['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36'],
			['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36'],
			['Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/38.0.2125.111 Chrome/38.0.2125.111 Safari/537.36'],
			['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/38.0.2125.111 Chrome/38.0.2125.111 Safari/537.36'],

			['Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0'],
			['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0'],
			['Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0'],
			['Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'],
			['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'],

			['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'],
			['Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'],
			['Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)'],
			['Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'],
			['Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'],

			['Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00'],
			['Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'],
			['Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'],
			['Opera/9.80 (Windows NT 6.1) Presto/2.12.388 Version/12.16'],
			['Opera/9.80 (Windows NT 6.1; Win64; x64) Presto/2.12.388 Version/12.17']
		])

	def randlogin(self):
		return random.choice([
			'idiocyxy','x3ajgnkrs13xtz','zavzema98','AssupRummubkt','empinhatn1','xxthinlovexxve','nagevolg05','Prahunmahvv',
			'zgurenimbn','valentnihnj','anonikelavs','Boutibi8q','mitelemkog5','atomize8v','etnologu1o','ze2ta2c8v',
			'nakrenu46','Scheuchea9','aefoxwillowqn','gollwngd1','aldo92200tg','pasjomny','strnoutjw','magsledefm',
			'bybelboekay','canaletto4v','sabinabr1234f','nagicamfr','trzaladh','nosie8','lustrous0v','nullvekst5t',
			'trissadork1','heynes2r','j3s2tgk','vises1b','maemotozq','ata2lapb6h','britneysboobspy','tomaiajl',
			'washaufurw','partieierqz','Math20','Ogulinkahny','pvillalobos2jm','rhagrasyskh','pinaybluele','aprilbloglp',
			'humorneur','obtahovatwp','agrafatgeuk','Entlerfp','BPOws','a2p1op1t26b','uchelafhc','crmdp',
			'mhuinntirqr','cohitarue','teampullzr','operculan7v','Ladidu6','MirmErronee62','errollawdz','searahlj',
			'g1intjy7','Alpenklubmj','Ektropion89','Auswuchsa5','freveltatua','o1kia5','iconhaveitxm','estrenhutfo',
			'Dipnainnaof','surras8b','quotexotasticvz','queculturaji','trueblonde71111','brigidashwoodrx','dreamfocusvy','kloptenzd',
			'ardalhatskd','supersayayin1n','glittery73bo','WeannamuPuv','masikipah','elblogdeinsai5w','Pedaleriek1','gbvideod3',
			'dragonhotnewsjt','FoumeVosem5','demagogisz3','vojnikev8','Sernau0h','luydduuf','orablerpaxopsc8','wrmbulletinoe',
			'lobaretzdh','ladyandria8g','madcow1041hc','malletad1','Elvisiorb','tenorytd8','angelicsnd','aber1r4',
			'2t1ar1cor2','Runtimew1','Ticenvibexh','zagabeeniee7','wokufaxj','gestormdhw','rezilcenn','duizelingr4',
			'majuzibx','deedee1307b1','pinkcheerios5g','gsusfreekdawnu6','konfetx1','nemizacaz8','klimopbos3m','ko2r1asztwp',
			'joelleferrete6y','iijokuoi0f','apozeugmasn','previsyh','pensionarja','Gaiarsanm','Neuansatzn3','burroughsman3l',
			'milenimvl','unapred3l','dekuncicy','Dawudte','smutnyrv','monsmons10','Domiblooria6z','dodawanies8',
			'torrent11p','hatedwords9x','aluhimrjn60','BopilkToola9j','ventverts9','Simeoli90','beiblatt8g','deposanrz',
			'Farbeimeroq','nijemca9x','ratelafq','wangelia777k0','Galestabs3c','o3mundosq5','lepidofitlx','mattdrew18qk',
			'agotaretzky','nakedsilencehd','jothepigy2','paiso1u','sjekteap','globojapi','pascut7v','desparetezx',
			'elegikerl7','agresszorci','dwarrowchild07','pomerilif2','maksillei9','Scibelliuh','Puncovhh','arturoonorio8q',
			'gmit6m','Briessekildrx','stebrcebr','WedLayexiaLabxc','tipicizezg1','Warburgerql','Moospadvavasf','NekOthepeke',
			'throwww','crogailln3','groorseZoog1v','Hurenbock1h','fuktigty','raspuste6z','bonkalw','varaularvn',
			'lemoncleansepm','Cabrol6b','frutseldemt','jujumevi2y','enzo90910sm','halfboy3y5','envadidorbr','flapkanre',
			'slavenkomw0','Rucmancemhe','CYMNBYNCVOK2h','z2jmw','entricasn8','clumsyshakess','wimberg04','ystormqz',
			'rollrgurl31zh','naklapalogp','Penzify','sxxxybaby1231y','marmoteisbv','uloviju1k','encoresseh6','crecianin',
			'jetledeeshorsdr','glockech','aidee18spainy1','BouswrareeCorsm','wingtsang2009s6','miseriaphyn97','xliddoxangelx2m','Erartooheriaf8d',
			'kilichokol2','garoxb','depletiv46','wudabumha','o2e1maij','Roulett02','ashelleystar3g','Trnovemuu4',
			'Csato00','betisinfodw','timexturner6v','lurkumjk','prvoborecvl','Pektenosetw','agulhoat0c','bancaladan8',
			'ocotlan2e','st4ie6j','Cohesdps','Jozzinofe','Eltzetj','edumnRogdregoms','tandwerk7b','keberioti6r',
			'konzilijex6','xskallelujahxa1','Szramowomu','pinksoda30084','garguiletz','disco2discoze','asignatk1q','DemOrenueDookqr',
			'yeggmh','bailaratzmo','zasutimaf8','Volksmund33','Dirmintiqg','wynwynyh','biollaiodiblegy','secretaresp',
			'tresutsla','insuranxnns5','werekanace','Varvellixy','nashinandaz3','preluderoninnl','aturdido1c','przybitka56',
			'vedricom4w','visualedgare1','Anagenese5z','Waldteilv1','fylliligavs','parsiemtijq','Affeflytemy57','maddi6665r',
			'mshihirix5','renareneli','Gnevsdorf0v','Cerigato8w','jrpantalim','mejicanofv','lanosasjn','thehulkstoygw',
			'acard39','tulpenbed9c','bamazeiz','Gezirph4','szmerekgr','atkilusqv','USAswk','aveusidaspw',
			'Karftwr','rhen21083u','Edelherrb5','sklonitexi','bbostate200u','premostila3','Hentzels9','chentexblogg8',
			'nebhandeib','stormdeib','illichbuilsn8','uilogymk','dyftykxu','custodianrg','rotace2q','spaposteodsvi',
			'iskrcaloo7','Iantaffi0f','goriStoottewu','pe3r2onas','misterjsonqi','newnightmarete','friend17ix','lojanoih',
			'Floressele','emali49','feblaire85','Arameespr','Pleldcerdemx0','turjainj','clairelascauxbd','bankobrevun',
			'nibris9a','quoteiliciouss6','angfersure2q','gwmpasall','Opponacamicoxav','magolents4l','abgeguckt5v','nemirnim82',
			'Attinsvenc0','Bikinic4','hollvini9w','sz3s2rx3','Miragalliw5','droitdusagev3','toady12bo','amrantunas9',
			'Skactweewvv','Steandodofadeea','exharacamni','umerilort5','guindarql','letopisom04','sars0116jd','odsiewaczgp',
			'Laxaxiovab2','CorsCoide0k','phasiwedeuf','sebansow9','papitosolteroj7','webpensieroul','puposoj7','Geraultan',
			'DymnkeypeDoffbi','Algownegorigejn','umniniyofx','romporaxe','misvan93mn','inchex','conger39','Husckovickf',
			'minciunowp','thepookguyt0','becknay5','Thurner3u','zasipanojav','fresalyz','lagosphere1g','kesiaaaaa9l',
			'emuttogeddyft','ae2pezi','gebuttertuz','glukozamixr','Pugljemo6','pembiusmv','Partitam4','unaniemut',
			'Seekanneds','malungelowh','AR8oy','van3000q5','Caile9w','imacephelmKamfn','cotsant3v','hakutuliayg',
			'imbornalk1','msgpusherc5','ghionoie2','Scabbiolo2r','Azad4o','espadelatke','itiparanoid13h3','K8CTZAE0k',
			'j0j0fansyb','elcalvoinvitabb','izmailicimv','ersatzub','periheliuh3','rovovskadi','seguicollaraw','rhodib2',
			'Kandoraeb','ariup3t','Musarjev9b','Kindhardri','diarejamihw','sunandgamesii','krypinaje','drip21lc',
			'fajansamal9','Saipan3s','scenarijacm','tubrhrkz9','fraktinj8','oporowieczm','Galfanozr','miquelcasals0k',
			'kuranskoj2i','rovito6d','venteprimo1','e3rumqa','istrebihbj','trebuiau3g','atupatzbq','Irraragocakepdt',
			'sintagmamii','bi1laeh','5pawkf','vaginmw','pastelcupcakeok','zeefactorf8','severuluieg','crysenc5',
			'matresrz','Tyncdercard9z','turdidesaz','gewelnaam23','hinziehen2i','pegreedilydaynw','pazaroll5','comattaip6g',
			'Wicewoo7','ipicaslj','rehabyuo','heiliasetfx','mediasferasie','Doonvatantanow1','luxatsu2','discounsyxv8',
			'longiadusl','darkdirkre','zagorze6g','ffiwdal8h','remirava85','Santiannif6','virekipirb','dukinoge2',
			'aeast317xe','blogmgqq','greenteaxoa9','Kompasuum','skourosekj','dekadischsh','go2r1e2lse','predisent4y',
			'exile23pt','rishigoqp','loiswanglingsz','zegget3','espirant9g','Paulinawf','mesmotsblogla','dukeblue3100tk',
			'veldua0','Engakycanny15','protkanu7r','islamomv3','WibleDumDoobej5','marcadius27','sajastegai6','codothi',
			'ParlFedaTarieca','Remorinoyg','Cagnolato63','doceerde25','seneVemeshorm04','encrestanmo','letst5k','pus1an2yjw',
			'desbardisi8','Eleltyzexxm','rudejaset','taffy1957u7','xoxobabes215h3','1JF6W5TO35','namahac6','dakgrasps',
			'deeltji','Zanollo8o','ubervolksmd','alyreneeqn','SnulleynC92','Kiestra7b','wilfredmong24','Jizba2e',
			'decadere9w','rispiglp','sammiebugev','Fexwoossyb1','uthiwea2','rutelk0','migradazf','Garitox0',
			'teletipesgg','mitomansb7','Belloneuf','thoirh3','krizoji5','elcabogne4w','pengeverdzo','estivatzo5',
			'propirioxt','chamuyamosargen','silverhillmv','osmotriteqg','il1blqr','kieuholtevt','odgojnojyj','mybsterw3',
			'Grabeland5w','laminato8s','brukkencp','izrecitewj','journaldexcogi','dekadamidz','recargatzpt','musivischf9',
			'glavarom8h','aubavaqf','lildrummagurluv','dorkogrande16pw','ruthieberk7o','reapudembr','Bacciani88','azizaju',
			'yndislegu84','niedurno4g','freakypryncez79','binnetrekvx','Realduccels02','Bleifarbev7','Affeldleaps00','caitgoesrarr6i',
			'skater7170vw','pokrovcemcv','Llangoeddy','Armeenjerxd','falquear77','rasierqv','Saraspitsn3','anmelde1r',
			'Faltenbaunu','aparentas2b','sur3n417z','filtrable2m','myescaperoute6s','moldrokixn','Prascafh','Franckinbw',
			'cyllellh8','klargjerecy','iwapoj2','cymhellom3b','akaofg','rabanhejp','Osmundw9','nazizm3w','Capuni8c',
			'poseermei6','noilliormem70','oplugtingye','szaladhat43','drpsalk6','nomerompandw','mornege2q','Aasmundc0',
			'Geraunzgy','Minotaurnw','firehead41vn','zuwettern3r','Lassig0e','lainemoutaineaq','club85uk','sachouuz',
			'timelipp9x','oscinmemn3e','zaprekama4k','gudangm4','dyemeng8','shaltairt5z','zingarsll'
		])

	def randtitle(self):
		return random.choice([
			'eating', 'sleeeepingggg', 'test', 'Hello, world',
			'cool stuff', 'i feel bad', 'Doctor, please help!',
			'Check my heart', 'i\'m tired', 'Lunch', 'dinner',
			'eat food', 'sit at table', 'do my homework',
			'go up the stairs', 'RUN', 'outdoor', 'walk',
			'up the hill', 'gogo', 'oh', 'auch', 'SnooZe',
			'TEST', 'check', 'work', 'watch TV', 'Play chess',
			'hospital', 'GOOD', 'yeah!', 'qwerty', '123'
		])

	def randalert(self):
		if random.randrange(0, 10) != 0:
			return self.randphrase()
		return random.choice([
			'died', 'alert', 'WARN', 'OMG!', 'Call doctor', 'my heart!!', 'What happened',
			'AAAAAAAAAAAAA', 'check it', 'LOOK AT THIS', 'Help', 'danger', 'qwety', 'test'
		])

	def randuser(self, randlen):
		login = uuid.uuid4().hex[:randlen]
		passlen = random.randrange(4, 10)
		password = uuid.uuid4().hex[:passlen]
		return {'login':self.randlogin() + login, 'pass':password}

	def randpoint(self, flag_id, flag):
		rnd = random.randrange(50, 100)
		if not flag:
			return {'val':rnd}
		event = flag
		if random.randrange(0, 5) == 0:
			event = self.randtitle() + ' ' + flag
		return {'val':rnd, 'evt':event}

	def randexpr(self):
		delim = self.randsp() + ',' + self.randsp()
		decpoint = '.'
		trueword = '"true"'
		falseword = '"false"'
		cond = random.choice(['<', '>', '<=', '>=', '=', '<>'])
		func = random.choice(['Avg', 'Median', 'StdDev', 'Max', 'Min', 'Last'])
		value = str(random.randrange(50, 100))
		if random.randrange(0, 1) == 1:
			value += decpoint
			value += str(random.randrange(1, 9))
		return 'if' + self.randsp() + '(' + self.randsp() + func + self.randsp() + '(' + self.randsp() + 'stat' + self.randsp() + ')' + self.randsp() + cond + self.randsp() + value + delim + trueword + delim + falseword + self.randsp() + ')'

	def randtruesubexpr(self, points):
		cond = random.choice(['<', '>', '<=', '>=', '=', '<>'])
		func = random.choice(['Avg', 'Median', 'StdDev', 'Max', 'Min', 'Last'])
		value = 0
		if cond in ['>', '>=']:
			if func != 'StdDev':
				value = random.randrange(0, 49)
			else:
				value = -random.randrange(1, 100)
		if cond in ['<', '<=', '<>']:
			if func != 'StdDev':
				value = random.randrange(101, 199)
			else:
				value = random.randrange(51, 100)
		if cond == '=':
			func = 'Last'
			value = self.findlast(points)
		if cond != '=' and random.randrange(0, 2) == 1:
			value += random.randrange(1, 100) / 100
		return func + self.randsp() + '(' + self.randsp() + 'stat' + self.randsp() + ')' + self.randsp() + cond + self.randsp() + str(value)

	def randtrueexpr(self, points, alert):
		decpoint = '.'
		trueword = '"' + alert + '"'
		falseword = 'null'
		if random.randrange(0, 10) == 0:
			falseword = '"' + self.randsp() + self.randword() + self.randsp() + '"'
		delim = self.randsp() + ',' + self.randsp()
		subexpr = self.randtruesubexpr(points)
		for i in range(0, random.randrange(0, 2)):
			op = random.choice([' and ', ' or '])
			subexpr += self.randsp() + op + self.randsp() + self.randtruesubexpr(points)
		return 'if' + self.randsp() + '(' + self.randsp() + subexpr + delim + self.randsp() + trueword + self.randsp() + delim + self.randsp() + 'null' + self.randsp() + ')'

	def findlast(self, points):
		last = points[0]
		for point in points:
			if point:
				last = point;
		return last.get('val')

	def randsp(self):
		spaces = '   '
		return spaces[:random.randrange(0, 2)]

	def get(self, addr, flag_id, flag):
		s = self.session(addr)

		result = self.sget(s, addr, '/login.html')
		if not result or len(result) == 0:
			print('get /login.html failed')
			return EXITCODE_MUMBLE

		parts = flag_id.split(':', 2)
		user = {'login':parts[0], 'pass':parts[1]}

		self.debug(user)

		result = self.spost(s, addr, '/signin/', user)
		if not result or result != 'OK':
			print('login failed')
			return EXITCODE_MUMBLE

		result = self.jget(s, addr, '/series/')
		if not result:
			print('points not found')
			return EXITCODE_MUMBLE

		points = result.get('points')
		if not points or len(points) == 0:
			print('points not found')
			return EXITCODE_CORRUPT

		event = ''
		for index, item in enumerate(points):
			evt = item.get('evt')
			if evt and len(evt) != 0:
				event = evt
				break

		if not ((event and event.find(flag) >= 0)):
			print('flag not found')
			return EXITCODE_CORRUPT

		return EXITCODE_OK

	def put(self, addr, flag_id, flag):
		s = self.session(addr)

		result = self.sget(s, addr, '/register.html')
		if not result or len(result) == 0:
			print('get /register.html failed')
			return EXITCODE_MUMBLE

		user = self.randuser(3)
		self.debug(user)

		for i in range(0, 3):
			try:
				result = self.spost(s, addr, '/signup/', user)
				if not result or result != 'OK':
					print('registration failed')
					return EXITCODE_MUMBLE

				break
			except HttpWebException as e:
				if e.value == 409:
					user = self.randuser(i * 5)
				else:
					raise

		point0 = None
		if random.randrange(0, 4) == 0:
			point0 = self.randpoint(flag_id, '')
			self.debug(point0)

			result = self.spost(s, addr, '/add/', point0)
			if not result or result != 'OK':
				print('add point failed')
				return EXITCODE_MUMBLE

		point1 = self.randpoint(flag_id, flag)
		self.debug(point1)

		result = self.spost(s, addr, '/add/', point1)
		if not result or result != 'OK':
			print('add point failed')
			return EXITCODE_MUMBLE

		point2 = None
		if random.randrange(0, 4) == 0:
			point2 = self.randpoint(flag_id, '')
			self.debug(point2)

			result = self.spost(s, addr, '/add/', point2)
			if not result or result != 'OK':
				print('add point failed')
				return EXITCODE_MUMBLE

		alert = self.randalert()

		expr = {'expr': self.randtrueexpr([point0, point1, point2], alert)}
		self.debug(expr)

		result = self.spost(s, addr, '/setexpr/', expr)
		if not result or result != 'OK':
			print('set expression failed')
			return EXITCODE_MUMBLE

		result = self.jget(s, addr, '/alerts/')
		if not result or result.get('msg') != alert:
			print('alert not found')
			return EXITCODE_MUMBLE

		print('{}:{}'.format(user['login'], user['pass']))
		return EXITCODE_OK

Checker().run()
