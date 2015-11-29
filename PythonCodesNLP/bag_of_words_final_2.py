import numpy
import nltk
import re
import csv
import scipy
import scipy.sparse
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
#nltk.download()
from nltk import pos_tag
_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
tagger = nltk.data.load(_POS_TAGGER)
import mysql.connector

from nltk.corpus import stopwords
print stopwords.words("english")
stops=stopwords.words("english")
stops.append("the")
stops.append("this")
stops.append("to")
stops.append("they")
stops.append("cause")
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None,stop_words = None)

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    else:
        return 'n'
		
def convert_words(data,stops):
     #print "hi";
     data=data.replace("=01","")
     data=data.replace("=09","")
     data=data.replace("=20"," ")
     data=data.replace("=","")
     data=data.replace("&nbsp"," ")
     data=re.sub('[\.,\,,\#,\!,\&,\@,\?,\:,\;,\>,\"]'," ",data)
     words=data.lower().split();
     
     meaningful_words = [w for w in words if not w in stops]
     tags=tagger.tag(meaningful_words)
     final_word_list=[]
     for tag in tags:
        #print tag[1] 
        type=get_wordnet_pos(tag[1])
        final_word_list.append(wnl.lemmatize(tag[0],type))	
     return( " ".join(final_word_list))
	 
cnx = mysql.connector.connect(user='root', database='enron_merged',password='root',host='localhost')
cursor = cnx.cursor();

cnx2 = mysql.connector.connect(user='root', database='enron_merged',password='root',host='localhost')
cursor2 = cnx2.cursor();
#query=("SELECT body,message_id from messages where split='TRAINING' and sender in (\"jeff.dasovich@enron.com\",\"kay.mann@enron.com\",\"sara.shackleton@enron.com\",\"tana.jones@enron.com\",\"vince.kaminski@enron.com\",\"chris.germany@enron.com\",\"no.address@enron.com\",\"enron.announcements@enron.com\",\"matthew.lenhart@enron.com\",\"debra.perlingiere@enron.com\",\"pete.davis@enron.com\",\"gerald.nemec@enron.com\",\"mark.taylor@enron.com\",\"40enron@enron.com\",\"carol.clair@enron.com\",\"steven.kean@enron.com\",\"eric.bass@enron.com\",\"richard.sanders@enron.com\",\"d..steffes@enron.com\",\"sally.beck@enron.com\",\"john.arnold@enron.com\",\"elizabeth.sager@enron.com\",\"outlook.team@enron.com\",\"louise.kitchen@enron.com\",\"kate.symes@enron.com\",\"susan.scott@enron.com\",\"j.kaminski@enron.com\",\"michelle.cash@enron.com\",\"kimberly.watson@enron.com\",\"john.lavorato@enron.com\",\"lynn.blair@enron.com\",\"jeffrey.shankman@enron.com\",\"drew.fossum@enron.com\",\"chris.dorland@enron.com\",\"marie.heard@enron.com\",\"mark.haedicke@enron.com\",\"benjamin.rogers@enron.com\",\"mike.grigsby@enron.com\",\"phillip.love@enron.com\",\"m..presto@enron.com\",\"susan.mara@enron.com\",\"kim.ward@enron.com\",\"david.delainey@enron.com\",\"mike.mcconnell@enron.com\",\"darron.giron@enron.com\",\"rod.hayslett@enron.com\",\"shelley.corman@enron.com\",\"james.derrick@enron.com\",\"daren.farmer@enron.com\",\"robin.rodrigue@enron.com\",\"announcements.enron@enron.com\",\"dan.hyvl@enron.com\",\"scott.neal@enron.com\",\"m..love@enron.com\",\"richard.shapiro@enron.com\",\"michelle.lokay@enron.com\",\"arsystem@mailman.enron.com\",\"phillip.allen@enron.com\",\"kevin.hyatt@enron.com\",\"rosalee.fleming@enron.com\",\"mary.cook@enron.com\",\"rick.buy@enron.com\",\"darrell.schoolcraft@enron.com\",\"joe.parks@enron.com\",\"exchangeinfo@nymex.com\",\"dutch.quigley@enron.com\",\"m..scott@enron.com\",\"david.forster@enron.com\",\"james.steffes@enron.com\",\"larry.campbell@enron.com\",\"taylor@enron.com\",\"barry.tycholiz@enron.com\",\"kam.keiser@enron.com\",\"ginger.dernehl@enron.com\",\"w..white@enron.com\",\"j..kean@enron.com\",\"errol.mclaughlin@enron.com\",\"matt.smith@enron.com\",\"stanley.horton@enron.com\",\"cara.semperger@enron.com\",\"mark.whitt@enron.com\",\"leslie.hansen@enron.com\",\"stephanie.panus@enron.com\",\"jae.black@enron.com\",\"enron_update@concureworkplace.com\",\"m..forney@enron.com\",\"karen.denne@enron.com\",\"tracy.geaccone@enron.com\",\"andy.zipper@enron.com\",\"mjones7@txu.com\",\"soblander@carrfut.com\",\"mark.greenberg@enron.com\",\"lavorato@enron.com\",\"lorna.brennan@enron.com\",\"m..schmidt@enron.com\",\"maureen.mcvicker@enron.com\",\"perfmgmt@enron.com\",\"alan.comnes@enron.com\",\"b..sanders@enron.com\",\"a..shankman@enron.com\",\"feedback@intcx.com\",\"stacey.white@enron.com\",\"john.zufferli@enron.com\",\"noreply@ccomad3.uu.commissioner.com\",\"dana.davis@enron.com\",\"tori.kuykendall@enron.com\",\"sheila.glover@enron.com\",\"lindy.donoho@enron.com\",\"veronica.espinoza@enron.com\",\"k..allen@enron.com\",\"jonathan.mckay@enron.com\",\"c..giron@enron.com\",\"hunter.shively@enron.com\",\"david.oxley@enron.com\",\"mike.carson@enron.com\",\"audrey.robertson@enron.com\",\"chairman.ken@enron.com\",\"office.chairman@enron.com\",\"sherri.sera@enron.com\",\"janette.elbertson@enron.com\",\"t..lucci@enron.com\",\"christi.nicolay@enron.com\",\"cooper.richey@enron.com\",\"tim.belden@enron.com\",\"v.weldon@enron.com\",\"evelyn.metoyer@enron.com\",\"cheryl.nelson@enron.com\",\"mark.mcconnell@enron.com\",\"m..tholt@enron.com\",\"marketing@nymex.com\",\"exchange.administrator@enron.com\",\"wsmith@wordsmith.org\",\"susan.bailey@enron.com\",\"victor.lamadrid@enron.com\",\"rhonda.denton@enron.com\",\"sarah.novosel@enron.com\",\"mary.hain@enron.com\",\"owner-eveningmba@haas.berkeley.edu\",\"kenneth.thibodeaux@enron.com\",\"kaminski@enron.com\",\"liz.taylor@enron.com\",\"sgovenar@govadv.com\",\"patrice.mims@enron.com\",\"alan.aronowitz@enron.com\",\"brent.hendry@enron.com\",\"monika.causholli@enron.com\",\"kerri.thompson@enron.com\",\"ben.jacoby@enron.com\",\"kevin.ruscitti@enron.com\",\"jane.tholt@enron.com\",\"miyung.buster@enron.com\",\"twanda.sweet@enron.com\",\"jason.williams@enron.com\",\"joseph.alamo@enron.com\",\"j..farmer@enron.com\",\"newsletter@rigzone.com\",\"greg.whalley@enron.com\",\"karen.buckley@enron.com\",\"bill.iii@enron.com\",\"judy.hernandez@enron.com\",\"a..martin@enron.com\",\"stacy.dickson@enron.com\",\"don.baughman@enron.com\",\"paul.kaufman@enron.com\",\"rob.gay@enron.com\",\"kevin.presto@enron.com\",\"taffy.milligan@enron.com\",\"shona.wilson@enron.com\",\"l..mims@enron.com\",\"info@pmaconference.com\",\"stephanie.miller@enron.com\",\"ina.rangel@enron.com\",\"nytdirect@nytimes.com\",\"tanya.rohauer@enron.com\",\"cheryl.johnson@enron.com\",\"michael.tribolet@enron.com\",\"fool@motleyfool.com\",\"beth.cherry@enform.com\",\"paul.y barbo@enron.com\",\"owner-nyiso_tech_exchange@lists.thebiz.net\",\"holly.keiser@enron.com\",\"ann.schmidt@enron.com\",\"shirley.crenshaw@enron.com\",\"martin.cuilla@enron.com\",\"jim.schwieger@enron.com\",\"danny.mccarty@enron.com\",\"robert.cotten@enron.com\",\"bob.shults@enron.com\",\"randall.gay@enron.com\",\"nancy.sellers@robertmondavi.com\",\"ami.chokshi@enron.com\",\"gelliott@industrialinfo.com\",\"jeffery.fawcett@enron.com\",\"amy.fitzpatrick@enron.com\",\"administration.enron@enron.com\",\"becky.spencer@enron.com\",\"janel.guerrero@enron.com\",\"issuealert@scientech.com\",\"center.ets@enron.com\",\"j..sturm@enron.com\",\"ecenter@williams.com\",\"lisa.yoho@enron.com\",\"brant.reves@enron.com\",\"outlook-migration-team@enron.com\",\"jerry.graves@enron.com\",\"david.minns@enron.com\",\"mday@gmssr.com\",\"gfergus@brobeck.com\",\"s..shively@enron.com\",\"robert.bruce@enron.com\",\"peter.keohane@enron.com\",\"keegan.farrell@enron.com\",\"l..nicolay@enron.com\",\"eric.gillaspie@enron.com\",\"savita.puthigai@enron.com\",\"stephanie.sever@enron.com\",\"jan.moore@enron.com\",\"diana.scholtes@enron.com\",\"theresa.staab@enron.com\",\"vkaminski@aol.com\",\"bill.rapp@enron.com\",\"sean.crandall@enron.com\",\"glen.hass@enron.com\",\"lgoldseth@svmg.org\",\"public.relations@enron.com\",\"marcus.nettelton@enron.com\",\"geoff.storey@enron.com\",\"russell.diamond@enron.com\",\"ray.alvarez@enron.com\",\"d..thomas@enron.com\",\"w..cantrell@enron.com\",\"carrfuturesenergy@carrfut.com\",\"lorraine.lindberg@enron.com\",\"linda.robertson@enron.com\",\"e..haedicke@enron.com\",\"holden.salisbury@enron.com\",\"chris.foster@enron.com\",\"david.portz@enron.com\",\"brian.redmond@enron.com\",\"britt.davis@enron.com\",\"justin.boyd@enron.com\",\"sandra.brawner@enron.com\",\"samantha.boyd@enron.com\",\"mark.palmer@enron.com\",\"juan.hernandez@enron.com\",\"f..calger@enron.com\",\"shari.stack@enron.com\",\"joannie.williamson@enron.com\",\"dennis.lee@enron.com\",\"bryant@cheatsheets.net\",\"sylvia.hu@enron.com\",\"chairman.enron@enron.com\",\"travis.mccullough@enron.com\",\"craig.buehler@enron.com\",\"jbennett@gmssr.com\",\"carol.st.@enron.com\",\"l..denton@enron.com\",\"harry.kingerski@enron.com\",\"kristin.walsh@enron.com\",\"leonardo.pacheco@enron.com\",\"andrea.ring@enron.com\",\"a..howard@enron.com\",\"stephanie.piwetz@enron.com\",\"mike.maggi@enron.com\",\"mark.schroeder@enron.com\",\"teb.lokey@enron.com\",\"tammie.schoppe@enron.com\",\"t..hodge@enron.com\",\"lisa.mellencamp@enron.com\",\"suzanne.adams@enron.com\",\"julie.armstrong@enron.com\",\"schwabalerts.marketupdates@schwab.com\",\"sue.nord@enron.com\",\"courtney.votaw@enron.com\",\"monique.sanchez@enron.com\",\"elizabeth.brown@enron.com\",\"fletcher.sturm@enron.com\",\"kay.chapman@enron.com\",\"kay.young@enron.com\",\"rahil.jafry@enron.com\",\"s..bradford@enron.com\",\"samuel.schott@enron.com\",\"navigator@nisource.com\",\"tk.lohman@enron.com\",\"susan.pereira@enron.com\",\"john.griffith@enron.com\",\"continental_airlines_inc@coair.rsc01.com\",\"rcarroll@bracepatt.com\",\"heather.dunton@enron.com\",\"john.shelk@enron.com\",\"megan.parker@enron.com\",\"al@friedwire.com\",\"cgoering@nyiso.com\",\"gavin.dillingham@enron.com\",\"grace.rodriguez@enron.com\",\"john.buchanan@enron.com\",\"justin.rostant@enron.com\",\"don.miller@enron.com\",\"reagan.rorschach@enron.com\",\"steven.harris@enron.com\",\"sharen.cason@enron.com\",\"phillip.platter@enron.com\",\"kimberly.hillis@enron.com\",\"s..ward@enron.com\",\"jennifer.thome@enron.com\",\"laura.luce@enron.com\",\"alex@pira.com\",\"christian.yoder@enron.com\",\"cameron@perfect.com\",\"greg.piper@enron.com\",\"charles.weldon@enron.com\",\"master.amar@hoegh.no\",\"jean.mrha@enron.com\",\"ruth.concannon@enron.com\",\"amr.ibrahim@enron.com\",\"christina.valdez@enron.com\",\"mary.poorman@enron.com\",\"kathleen.carnahan@enron.com\",\"louis.dicarlo@enron.com\",\"rvujtech@carrfut.com\",\"jr..legal@enron.com\",\"patti.thompson@enron.com\",\"christopher.calger@enron.com\",\"stacey.bolton@enron.com\",\"melissa.murphy@enron.com\",\"edismail@incident.com\",\"c..williams@enron.com\",\"info@forexnews.com\",\"stuart.zisman@enron.com\",\"frank.hayden@enron.com\",\"ed.mcmichael@enron.com\",\"cynthia.sandherr@enron.com\",\"dale.neuner@enron.com\",\"pmadpr@worldnet.att.net\",\"c..gossett@enron.com\",\"abcnewsnow-editor@mail.abcnews.go.com\",\"andrew.edison@enron.com\",\"leslie.lawner@enron.com\",\"joe.stepenovitch@enron.com\",\"cindy.stark@enron.com\",\"stacey.richardson@enron.com\",\"david.port@enron.com\",\"lisa.gang@enron.com\",\"mark.guzman@enron.com\",\"geir.solberg@enron.com\",\"ryan.slinger@enron.com\",\"leaf.harasin@enron.com\",\"bert.meyers@enron.com\",\"craig.dean@enron.com\",\"eric.linder@enron.com\",\"bill.williams.iii@enron.com\",\"dporter3@enron.com\",\"jbryson@enron.com\",\"joe.hartsoe@enron.com\",\"sandra.mccubbin@enron.com\",\"kenneth.lay@enron.com\",\"william.bradford@enron.com\",\"tom.moran@enron.com\",\"jeffrey.hodge@enron.com\",\"jdasovic@enron.com\",\"bill.williams@enron.com\",\"edward.sacks@enron.com\",\"don.black@enron.com\",\"jeff.skilling@enron.com\",\"tracy.ngo@enron.com\",\"doug.gilbert-smith@enron.com\",\"mark.frevert@enron.com\",\"lloyd.will@enron.com\",\"steven.merris@enron.com\",\"vicki.sharp@enron.com\",\"leslie.reeves@enron.com\",\"skean@enron.com\",\"donna.fulton@enron.com\",\"john.sherriff@enron.com\",\"genia.fitzgerald@enron.com\",\"keith.holst@enron.com\",\"frank.sayre@enron.com\",\"jeff.richter@enron.com\",\"greg.wolfe@enron.com\",\"sheila.tweed@enron.com\",\"lisa.lees@enron.com\",\"robert.badeer@enron.com\",\"scott.goodell@enron.com\",\"janet.dietrich@enron.com\",\" All Enron Worldwide@ENRON\",\"rick.dietz@enron.com\",\"julia.murray@enron.com\",\"karen.lambert@enron.com\",\"jason.wolfe@enron.com\",\"ted.murphy@enron.com\",\"rogers.herndon@enron.com\",\"judy.townsend@enron.com\",\"dan.leff@enron.com\",\"jeffrey.mcmahon@enron.com\",\"klay@enron.com\",\"jay.reitmeyer@enron.com\",\"mona.petrochko@enron.com\",\"debbie.brackett@enron.com\",\"steve.walton@enron.com\",\"eric.saibi@enron.com\",\"michael.etringer@enron.com\",\"mike.swerzbin@enron.com\",\"robert.benson@enron.com\",\"terry.kowalke@enron.com\",\"bob.bowen@enron.com\",\"dennis.benevides@enron.com\",\"tom.may@enron.com\",\"elizabeth.linnell@enron.com\",\"wanda.curry@enron.com\",\"david.baumbach@enron.com\",\"jeffrey.miller@enron.com\",\"frank.ermis@enron.com\",\"mike.smith@enron.com\",\"sheri.thomas@enron.com\",\"mark.koenig@enron.com\",\"rob.milnthorp@enron.com\",\"jeff.king@enron.com\",\"jeremy.blachman@enron.com\",\"bryan.hull@enron.com\",\"robert.frank@enron.com\",\"corry.bentley@enron.com\",\"raymond.bowen@enron.com\",\"john.kinser@enron.com\",\"barbara.gray@enron.com\",\"clint.dean@enron.com\",\"richard.causey@enron.com\",\"wes.colwell@enron.com\",\"joe.errigo@enron.com\",\"paul.radous@enron.com\",\"patrick.hanse@enron.com\",\"john.viverito@enron.com\",\"harry.arora@enron.com\",\"c..koehler@enron.com\",\"chris.mallory@enron.com\",\"robert.superty@enron.com\",\"juan.padron@enron.com\",\"brad.mckay@enron.com\",\"r..brackett@enron.com\",\"rika.imai@enron.com\",\"shonnie.daniel@enron.com\",\"kaye.ellis@enron.com\",\"frank.vickers@enron.com\",\"kayne.coulter@enron.com\",\"l..gay@enron.com\",\"robert.neustaedter@enron.com\",\"angela.davis@enron.com\",\"steve.montovano@enron.com\",\"peter.makkai@enron.com\",\"tom.briggs@enron.com\",\"vladimir.gorny@enron.com\",\"marty.sunde@enron.com\",\"jim.fallon@enron.com\",\"all.worldwide@enron.com\",\"patti.sullivan@enron.com\",\"lisa.gillette@enron.com\",\"kevin.cline@enron.com\",\"robert.stalford@enron.com\",\"tom.alonso@enron.com\",\"harry.collins@enron.com\",\"mpalmer@enron.com\",\"gautam.gupta@enron.com\",\"jennifer.burns@enron.com\",\"f..brawner@enron.com\",\"fred.lagrasta@enron.com\",\"chris.gaskill@enron.com\",\"david.parquet@enron.com\",\"janine.migden@enron.com\",\"n..gray@enron.com\",\"larry.may@enron.com\",\"jason.choate@enron.com\",\"russell.ballato@enron.com\",\"doug.sewell@enron.com\",\"gerald.gilbert@enron.com\",\"frank.davis@enron.com\",\"mark.fischer@enron.com\",\"dean.laurent@enron.com\",\"sheila.nacey@enron.com\",\"lisa.burnett@enron.com\",\"maria.valdes@enron.com\",\" All Enron Houston@ENRON\",\"bill.rust@enron.com\",\"larry.valderrama@enron.com\",\"d..baughman@enron.com\",\"lance.schuler-legal@enron.com\",\"matt.motley@enron.com\",\"pinto.leite@enron.com\",\"p..south@enron.com\",\"daniel.allegretti@enron.com\",\"vladi.pimenov@enron.com\",\"john.hodge@enron.com\",\"dave.perrino@enron.com\",\"bernice.rodriguez@enron.com\",\"david.fairley@enron.com\",\"james.wright@enron.com\",\"mary.ogden@enron.com\",\"carol.moffett@enron.com\")")
#query=("SELECT body,message_id from messages where split='TRAINING' and sender in (\"jeff.dasovich@enron.com\",\"kay.mann@enron.com\",\"sara.shackleton@enron.com\",\"tana.jones@enron.com\",\"vince.kaminski@enron.com\",\"chris.germany@enron.com\",\"no.address@enron.com\",\"enron.announcements@enron.com\",\"matthew.lenhart@enron.com\",\"debra.perlingiere@enron.com\",\"pete.davis@enron.com\",\"gerald.nemec@enron.com\",\"mark.taylor@enron.com\",\"40enron@enron.com\",\"carol.clair@enron.com\",\"steven.kean@enron.com\",\"eric.bass@enron.com\",\"richard.sanders@enron.com\",\"d..steffes@enron.com\",\"sally.beck@enron.com\",\"john.arnold@enron.com\",\"elizabeth.sager@enron.com\",\"outlook.team@enron.com\",\"louise.kitchen@enron.com\",\"kate.symes@enron.com\",\"susan.scott@enron.com\",\"j.kaminski@enron.com\",\"michelle.cash@enron.com\",\"kimberly.watson@enron.com\",\"john.lavorato@enron.com\",\"lynn.blair@enron.com\",\"jeffrey.shankman@enron.com\",\"drew.fossum@enron.com\",\"chris.dorland@enron.com\",\"marie.heard@enron.com\",\"mark.haedicke@enron.com\",\"benjamin.rogers@enron.com\",\"mike.grigsby@enron.com\",\"phillip.love@enron.com\",\"m..presto@enron.com\",\"susan.mara@enron.com\",\"kim.ward@enron.com\",\"david.delainey@enron.com\",\"mike.mcconnell@enron.com\",\"darron.giron@enron.com\",\"rod.hayslett@enron.com\",\"shelley.corman@enron.com\",\"james.derrick@enron.com\",\"daren.farmer@enron.com\",\"robin.rodrigue@enron.com\",\"announcements.enron@enron.com\",\"dan.hyvl@enron.com\",\"scott.neal@enron.com\",\"m..love@enron.com\",\"richard.shapiro@enron.com\",\"michelle.lokay@enron.com\",\"arsystem@mailman.enron.com\",\"phillip.allen@enron.com\",\"kevin.hyatt@enron.com\",\"rosalee.fleming@enron.com\",\"mary.cook@enron.com\",\"rick.buy@enron.com\",\"darrell.schoolcraft@enron.com\",\"joe.parks@enron.com\",\"exchangeinfo@nymex.com\",\"dutch.quigley@enron.com\",\"m..scott@enron.com\",\"david.forster@enron.com\",\"james.steffes@enron.com\",\"larry.campbell@enron.com\",\"taylor@enron.com\",\"barry.tycholiz@enron.com\",\"kam.keiser@enron.com\",\"ginger.dernehl@enron.com\",\"w..white@enron.com\",\"j..kean@enron.com\",\"errol.mclaughlin@enron.com\",\"matt.smith@enron.com\",\"stanley.horton@enron.com\",\"cara.semperger@enron.com\",\"mark.whitt@enron.com\",\"leslie.hansen@enron.com\",\"stephanie.panus@enron.com\",\"jae.black@enron.com\",\"enron_update@concureworkplace.com\",\"m..forney@enron.com\",\"karen.denne@enron.com\",\"tracy.geaccone@enron.com\",\"andy.zipper@enron.com\",\"mjones7@txu.com\",\"soblander@carrfut.com\",\"mark.greenberg@enron.com\",\"lavorato@enron.com\",\"lorna.brennan@enron.com\",\"m..schmidt@enron.com\",\"maureen.mcvicker@enron.com\",\"perfmgmt@enron.com\",\"alan.comnes@enron.com\",\"b..sanders@enron.com\",\"a..shankman@enron.com\",\"feedback@intcx.com\",\"stacey.white@enron.com\",\"john.zufferli@enron.com\",\"noreply@ccomad3.uu.commissioner.com\",\"dana.davis@enron.com\",\"tori.kuykendall@enron.com\",\"sheila.glover@enron.com\",\"lindy.donoho@enron.com\",\"veronica.espinoza@enron.com\",\"k..allen@enron.com\",\"jonathan.mckay@enron.com\",\"c..giron@enron.com\",\"hunter.shively@enron.com\",\"david.oxley@enron.com\",\"mike.carson@enron.com\",\"audrey.robertson@enron.com\",\"chairman.ken@enron.com\",\"office.chairman@enron.com\",\"sherri.sera@enron.com\",\"janette.elbertson@enron.com\",\"t..lucci@enron.com\",\"christi.nicolay@enron.com\",\"cooper.richey@enron.com\",\"tim.belden@enron.com\",\"v.weldon@enron.com\",\"evelyn.metoyer@enron.com\",\"cheryl.nelson@enron.com\",\"mark.mcconnell@enron.com\",\"m..tholt@enron.com\",\"marketing@nymex.com\",\"exchange.administrator@enron.com\",\"wsmith@wordsmith.org\",\"susan.bailey@enron.com\",\"victor.lamadrid@enron.com\",\"rhonda.denton@enron.com\",\"sarah.novosel@enron.com\",\"mary.hain@enron.com\",\"owner-eveningmba@haas.berkeley.edu\",\"kenneth.thibodeaux@enron.com\",\"kaminski@enron.com\",\"liz.taylor@enron.com\",\"sgovenar@govadv.com\",\"patrice.mims@enron.com\",\"alan.aronowitz@enron.com\",\"brent.hendry@enron.com\",\"monika.causholli@enron.com\",\"kerri.thompson@enron.com\",\"ben.jacoby@enron.com\",\"kevin.ruscitti@enron.com\",\"jane.tholt@enron.com\",\"miyung.buster@enron.com\",\"twanda.sweet@enron.com\",\"jason.williams@enron.com\",\"joseph.alamo@enron.com\",\"j..farmer@enron.com\",\"newsletter@rigzone.com\",\"greg.whalley@enron.com\",\"karen.buckley@enron.com\",\"bill.iii@enron.com\",\"judy.hernandez@enron.com\",\"a..martin@enron.com\",\"stacy.dickson@enron.com\",\"don.baughman@enron.com\",\"paul.kaufman@enron.com\",\"rob.gay@enron.com\",\"kevin.presto@enron.com\",\"taffy.milligan@enron.com\",\"shona.wilson@enron.com\",\"l..mims@enron.com\",\"info@pmaconference.com\",\"stephanie.miller@enron.com\",\"ina.rangel@enron.com\",\"nytdirect@nytimes.com\",\"tanya.rohauer@enron.com\",\"cheryl.johnson@enron.com\",\"michael.tribolet@enron.com\",\"fool@motleyfool.com\",\"beth.cherry@enform.com\",\"paul.y barbo@enron.com\",\"owner-nyiso_tech_exchange@lists.thebiz.net\",\"holly.keiser@enron.com\",\"ann.schmidt@enron.com\",\"shirley.crenshaw@enron.com\",\"martin.cuilla@enron.com\",\"jim.schwieger@enron.com\",\"danny.mccarty@enron.com\",\"robert.cotten@enron.com\",\"bob.shults@enron.com\",\"randall.gay@enron.com\",\"nancy.sellers@robertmondavi.com\",\"ami.chokshi@enron.com\",\"gelliott@industrialinfo.com\",\"jeffery.fawcett@enron.com\",\"amy.fitzpatrick@enron.com\",\"administration.enron@enron.com\",\"becky.spencer@enron.com\",\"janel.guerrero@enron.com\",\"issuealert@scientech.com\",\"center.ets@enron.com\",\"j..sturm@enron.com\",\"ecenter@williams.com\",\"lisa.yoho@enron.com\",\"brant.reves@enron.com\",\"outlook-migration-team@enron.com\",\"jerry.graves@enron.com\",\"david.minns@enron.com\",\"mday@gmssr.com\",\"gfergus@brobeck.com\",\"s..shively@enron.com\",\"robert.bruce@enron.com\",\"peter.keohane@enron.com\",\"keegan.farrell@enron.com\",\"l..nicolay@enron.com\",\"eric.gillaspie@enron.com\",\"savita.puthigai@enron.com\",\"stephanie.sever@enron.com\",\"jan.moore@enron.com\",\"diana.scholtes@enron.com\",\"theresa.staab@enron.com\",\"vkaminski@aol.com\",\"bill.rapp@enron.com\",\"sean.crandall@enron.com\",\"glen.hass@enron.com\",\"lgoldseth@svmg.org\",\"public.relations@enron.com\",\"marcus.nettelton@enron.com\",\"geoff.storey@enron.com\",\"russell.diamond@enron.com\",\"ray.alvarez@enron.com\",\"d..thomas@enron.com\",\"w..cantrell@enron.com\",\"carrfuturesenergy@carrfut.com\",\"lorraine.lindberg@enron.com\",\"linda.robertson@enron.com\",\"e..haedicke@enron.com\",\"holden.salisbury@enron.com\",\"chris.foster@enron.com\",\"david.portz@enron.com\",\"brian.redmond@enron.com\",\"britt.davis@enron.com\",\"justin.boyd@enron.com\",\"sandra.brawner@enron.com\",\"samantha.boyd@enron.com\",\"mark.palmer@enron.com\",\"juan.hernandez@enron.com\",\"f..calger@enron.com\",\"shari.stack@enron.com\",\"joannie.williamson@enron.com\",\"dennis.lee@enron.com\",\"bryant@cheatsheets.net\",\"sylvia.hu@enron.com\",\"chairman.enron@enron.com\",\"travis.mccullough@enron.com\",\"craig.buehler@enron.com\",\"jbennett@gmssr.com\",\"carol.st.@enron.com\",\"l..denton@enron.com\",\"harry.kingerski@enron.com\",\"kristin.walsh@enron.com\",\"leonardo.pacheco@enron.com\",\"andrea.ring@enron.com\",\"a..howard@enron.com\",\"stephanie.piwetz@enron.com\",\"mike.maggi@enron.com\",\"mark.schroeder@enron.com\",\"teb.lokey@enron.com\",\"tammie.schoppe@enron.com\",\"t..hodge@enron.com\",\"lisa.mellencamp@enron.com\",\"suzanne.adams@enron.com\",\"julie.armstrong@enron.com\",\"schwabalerts.marketupdates@schwab.com\",\"sue.nord@enron.com\",\"courtney.votaw@enron.com\",\"monique.sanchez@enron.com\",\"elizabeth.brown@enron.com\",\"fletcher.sturm@enron.com\",\"kay.chapman@enron.com\",\"kay.young@enron.com\",\"rahil.jafry@enron.com\",\"s..bradford@enron.com\",\"samuel.schott@enron.com\",\"navigator@nisource.com\",\"tk.lohman@enron.com\",\"susan.pereira@enron.com\",\"john.griffith@enron.com\",\"continental_airlines_inc@coair.rsc01.com\",\"rcarroll@bracepatt.com\",\"heather.dunton@enron.com\",\"john.shelk@enron.com\",\"megan.parker@enron.com\",\"al@friedwire.com\",\"cgoering@nyiso.com\",\"gavin.dillingham@enron.com\",\"grace.rodriguez@enron.com\",\"john.buchanan@enron.com\",\"justin.rostant@enron.com\",\"don.miller@enron.com\",\"reagan.rorschach@enron.com\",\"steven.harris@enron.com\",\"sharen.cason@enron.com\",\"phillip.platter@enron.com\",\"kimberly.hillis@enron.com\",\"s..ward@enron.com\",\"jennifer.thome@enron.com\",\"laura.luce@enron.com\",\"alex@pira.com\",\"christian.yoder@enron.com\",\"cameron@perfect.com\",\"greg.piper@enron.com\",\"charles.weldon@enron.com\",\"master.amar@hoegh.no\",\"jean.mrha@enron.com\",\"ruth.concannon@enron.com\",\"amr.ibrahim@enron.com\",\"christina.valdez@enron.com\",\"mary.poorman@enron.com\",\"kathleen.carnahan@enron.com\",\"louis.dicarlo@enron.com\",\"rvujtech@carrfut.com\",\"jr..legal@enron.com\",\"patti.thompson@enron.com\",\"christopher.calger@enron.com\",\"stacey.bolton@enron.com\",\"melissa.murphy@enron.com\",\"edismail@incident.com\",\"c..williams@enron.com\",\"info@forexnews.com\",\"stuart.zisman@enron.com\",\"frank.hayden@enron.com\",\"ed.mcmichael@enron.com\",\"cynthia.sandherr@enron.com\",\"dale.neuner@enron.com\",\"pmadpr@worldnet.att.net\",\"c..gossett@enron.com\",\"abcnewsnow-editor@mail.abcnews.go.com\",\"andrew.edison@enron.com\",\"leslie.lawner@enron.com\",\"joe.stepenovitch@enron.com\",\"cindy.stark@enron.com\",\"stacey.richardson@enron.com\",\"david.port@enron.com\",\"lisa.gang@enron.com\",\"mark.guzman@enron.com\",\"geir.solberg@enron.com\",\"ryan.slinger@enron.com\",\"leaf.harasin@enron.com\",\"bert.meyers@enron.com\",\"craig.dean@enron.com\",\"eric.linder@enron.com\",\"bill.williams.iii@enron.com\",\"dporter3@enron.com\",\"jbryson@enron.com\",\"joe.hartsoe@enron.com\",\"sandra.mccubbin@enron.com\",\"kenneth.lay@enron.com\",\"william.bradford@enron.com\",\"tom.moran@enron.com\",\"jeffrey.hodge@enron.com\",\"jdasovic@enron.com\",\"bill.williams@enron.com\",\"edward.sacks@enron.com\",\"don.black@enron.com\",\"jeff.skilling@enron.com\",\"tracy.ngo@enron.com\",\"doug.gilbert-smith@enron.com\",\"mark.frevert@enron.com\",\"lloyd.will@enron.com\",\"steven.merris@enron.com\",\"vicki.sharp@enron.com\",\"leslie.reeves@enron.com\",\"skean@enron.com\",\"donna.fulton@enron.com\",\"john.sherriff@enron.com\",\"genia.fitzgerald@enron.com\",\"keith.holst@enron.com\",\"frank.sayre@enron.com\",\"jeff.richter@enron.com\",\"greg.wolfe@enron.com\",\"sheila.tweed@enron.com\",\"lisa.lees@enron.com\",\"robert.badeer@enron.com\",\"scott.goodell@enron.com\",\"janet.dietrich@enron.com\",\" All Enron Worldwide@ENRON\",\"rick.dietz@enron.com\",\"julia.murray@enron.com\",\"karen.lambert@enron.com\",\"jason.wolfe@enron.com\",\"ted.murphy@enron.com\",\"rogers.herndon@enron.com\",\"judy.townsend@enron.com\",\"dan.leff@enron.com\",\"jeffrey.mcmahon@enron.com\",\"klay@enron.com\",\"jay.reitmeyer@enron.com\",\"mona.petrochko@enron.com\",\"debbie.brackett@enron.com\",\"steve.walton@enron.com\",\"eric.saibi@enron.com\",\"michael.etringer@enron.com\",\"mike.swerzbin@enron.com\",\"robert.benson@enron.com\",\"terry.kowalke@enron.com\",\"bob.bowen@enron.com\",\"dennis.benevides@enron.com\",\"tom.may@enron.com\",\"elizabeth.linnell@enron.com\",\"wanda.curry@enron.com\",\"david.baumbach@enron.com\",\"jeffrey.miller@enron.com\",\"frank.ermis@enron.com\",\"mike.smith@enron.com\",\"sheri.thomas@enron.com\",\"mark.koenig@enron.com\",\"rob.milnthorp@enron.com\",\"jeff.king@enron.com\",\"jeremy.blachman@enron.com\",\"bryan.hull@enron.com\",\"robert.frank@enron.com\",\"corry.bentley@enron.com\",\"raymond.bowen@enron.com\",\"john.kinser@enron.com\",\"barbara.gray@enron.com\",\"clint.dean@enron.com\",\"richard.causey@enron.com\",\"wes.colwell@enron.com\",\"joe.errigo@enron.com\",\"paul.radous@enron.com\",\"patrick.hanse@enron.com\",\"john.viverito@enron.com\",\"harry.arora@enron.com\",\"c..koehler@enron.com\",\"chris.mallory@enron.com\",\"robert.superty@enron.com\",\"juan.padron@enron.com\",\"brad.mckay@enron.com\",\"r..brackett@enron.com\",\"rika.imai@enron.com\",\"shonnie.daniel@enron.com\",\"kaye.ellis@enron.com\",\"frank.vickers@enron.com\",\"kayne.coulter@enron.com\",\"l..gay@enron.com\",\"robert.neustaedter@enron.com\",\"angela.davis@enron.com\",\"steve.montovano@enron.com\",\"peter.makkai@enron.com\",\"tom.briggs@enron.com\",\"vladimir.gorny@enron.com\",\"marty.sunde@enron.com\",\"jim.fallon@enron.com\",\"all.worldwide@enron.com\",\"patti.sullivan@enron.com\",\"lisa.gillette@enron.com\",\"kevin.cline@enron.com\",\"robert.stalford@enron.com\",\"tom.alonso@enron.com\",\"harry.collins@enron.com\",\"mpalmer@enron.com\",\"gautam.gupta@enron.com\",\"jennifer.burns@enron.com\",\"f..brawner@enron.com\",\"fred.lagrasta@enron.com\",\"chris.gaskill@enron.com\",\"david.parquet@enron.com\",\"janine.migden@enron.com\",\"n..gray@enron.com\",\"larry.may@enron.com\",\"jason.choate@enron.com\",\"russell.ballato@enron.com\",\"doug.sewell@enron.com\",\"gerald.gilbert@enron.com\",\"frank.davis@enron.com\",\"mark.fischer@enron.com\",\"dean.laurent@enron.com\",\"sheila.nacey@enron.com\",\"lisa.burnett@enron.com\",\"maria.valdes@enron.com\",\" All Enron Houston@ENRON\",\"bill.rust@enron.com\",\"larry.valderrama@enron.com\",\"d..baughman@enron.com\",\"lance.schuler-legal@enron.com\",\"matt.motley@enron.com\",\"pinto.leite@enron.com\",\"p..south@enron.com\",\"daniel.alleg\")"
#query=("SELECT body,mid from messages where split='TRAINING' and sender in (\"jeff.dasovich@enron.com\",\"kay.mann@enron.com\",\"sara.shackleton@enron.com\",\"tana.jones@enron.com\",\"vince.kaminski@enron.com\",\"chris.germany@enron.com\",\"no.address@enron.com\",\"enron.announcements@enron.com\",\"matthew.lenhart@enron.com\",\"debra.perlingiere@enron.com\",\"pete.davis@enron.com\",\"gerald.nemec@enron.com\",\"mark.taylor@enron.com\",\"40enron@enron.com\",\"carol.clair@enron.com\",\"steven.kean@enron.com\",\"eric.bass@enron.com\",\"richard.sanders@enron.com\",\"d..steffes@enron.com\",\"sally.beck@enron.com\",\"john.arnold@enron.com\",\"elizabeth.sager@enron.com\",\"outlook.team@enron.com\",\"louise.kitchen@enron.com\",\"kate.symes@enron.com\",\"susan.scott@enron.com\",\"j.kaminski@enron.com\",\"michelle.cash@enron.com\",\"kimberly.watson@enron.com\",\"john.lavorato@enron.com\",\"lynn.blair@enron.com\",\"jeffrey.shankman@enron.com\",\"drew.fossum@enron.com\",\"chris.dorland@enron.com\",\"marie.heard@enron.com\",\"mark.haedicke@enron.com\",\"benjamin.rogers@enron.com\",\"mike.grigsby@enron.com\",\"phillip.love@enron.com\",\"m..presto@enron.com\",\"susan.mara@enron.com\",\"kim.ward@enron.com\",\"david.delainey@enron.com\",\"mike.mcconnell@enron.com\",\"darron.giron@enron.com\",\"rod.hayslett@enron.com\",\"shelley.corman@enron.com\",\"james.derrick@enron.com\",\"daren.farmer@enron.com\",\"robin.rodrigue@enron.com\",\"announcements.enron@enron.com\",\"dan.hyvl@enron.com\",\"scott.neal@enron.com\",\"m..love@enron.com\",\"richard.shapiro@enron.com\",\"michelle.lokay@enron.com\",\"arsystem@mailman.enron.com\",\"phillip.allen@enron.com\",\"kevin.hyatt@enron.com\",\"rosalee.fleming@enron.com\",\"mary.cook@enron.com\",\"rick.buy@enron.com\",\"darrell.schoolcraft@enron.com\",\"joe.parks@enron.com\",\"exchangeinfo@nymex.com\",\"dutch.quigley@enron.com\",\"m..scott@enron.com\",\"david.forster@enron.com\",\"james.steffes@enron.com\",\"larry.campbell@enron.com\",\"taylor@enron.com\",\"barry.tycholiz@enron.com\",\"kam.keiser@enron.com\",\"mark.guzman@enron.com\",\"geir.solberg@enron.com\",\"paul.kaufman@enron.com\",\"ryan.slinger@enron.com\",\"leaf.harasin@enron.com\",\"bert.meyers@enron.com\",\"tim.belden@enron.com\",\"monika.causholli@enron.com\",\"craig.dean@enron.com\",\"eric.linder@enron.com\",\"harry.kingerski@enron.com\",\"greg.whalley@enron.com\",\"sarah.novosel@enron.com\",\"susan.bailey@enron.com\",\"bill.williams.iii@enron.com\",\"dporter3@enron.com\",\"jbryson@enron.com\",\"alan.comnes@enron.com\",\"karen.denne@enron.com\",\"linda.robertson@enron.com\",\"mark.palmer@enron.com\",\"joe.hartsoe@enron.com\",\"steven.harris@enron.com\",\"stephanie.panus@enron.com\",\"sandra.mccubbin@enron.com\")")
query=("SELECT body,mid from messages where split='TRAINING' and mid in (209765,209766,209769)");
cursor.execute(query);
cleaned_data=[];
id=[];
stops = set(stops)
f=open('log_document_term_latest.txt','w')
f1=open('document_term_exceptions.txt','w')
index=0
for body,mid in cursor:
     cleaned_string=convert_words(body,stops);
     cleaned_data.append(cleaned_string);
     id.append(mid)
for item in id:
       f.write(str(item))
       f.write(",")	   
###to test-    
########cleaned_data=["i am sukriti. this is is my story.","I was born in india. I have a younger brother.","I am now pursuing masters."]

word_features=vectorizer.fit_transform(cleaned_data);
a=word_features.getrow(0).toarray()
print word_features.getrow(0).toarray()
print word_features
####word_features = word_features.toarray()
####print word_features[0]
#print word_features.shape()
vocab = vectorizer.get_feature_names()
#print vocab
print len(vocab)
a=scipy.sparse.find(word_features)
row=a[0]
col=a[1]
vals=a[2]
for i in range(0,len(row)):
    #print " doc ",row[i]," term ",vocab[col[i]]," count ",vals[i]
    doc_term=(id[row[i]],vocab[col[i]],vals[i])
    try:
         cursor2.execute("insert into document_term (number,term,count) values (%d,\'%s\',%d)"%doc_term)
         print cursor2.statement
         f.write(cursor2.statement)
         f.write("\n")
    except mysql.connector.Error as e:
            f.write(e.msg)
            f.write("\n")
            fl.write(e.msg)
            f1.write("\n")
    cnx2.commit();
""""
with open('bag_of_words.csv','wb') as f:
     csv.writer(f).writerow(vocab)
     for i in range(0,252759):
        a=word_features.getrow(i).toarray()
        numpy.savetxt(f,a,delimiter=",")
     ###csv.writer(f).writerow(word_features.getrow(0).toarray())
	 """
#####################3f.close()
f.close()
f1.close()
cnx.close()
cnx2.close()