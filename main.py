import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App

from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button

import json

# +----------------------------------+
# | StackLayout                      |
# | +------------------------------+ |
# | | ScrollView                   | |
# | | +----------------------+  ^  | |
# | | | StackLayout          | | | | |
# | | | +-++---------------+ | | | | |
# | | | |x||Label          | | | | | |
# | | | +-++---------------+ | | | | |
# | | | +-++---------------+ | | | | |
# | | | |x||Label          | | | | | |
# | | | +-++---------------+ | | | | |
# | | | +-++---------------+ | | | | |
# | | | |x||Label          | | | | | |
# | | | +-++---------------+ | | | | |
# | | | +-++---------------+ | | | | |
# | | | |x||Label          | | | | | |
# | | | +-++---------------+ | | | | |
# | | |                      | | | | |
# | | +----------------------+  v  | |
# | +------------------------------+ |
# | +------------------------------+ |
# | | BoxLayout                    | |
# | |     +-+ +------+ +---------+ | |
# | | Hide|x| | Save | | Restore | | |
# | |     +-+ +------+ +---------+ | |
# | +------------------------------+ |
# +----------------------------------+

class CheckList(StackLayout):

    def __init__(self, **kwargs):
        super(CheckList, self).__init__(**kwargs)

        title = Label(
            text='Checker',
            size_hint=(1, .05),
            height = '30sp',
        )
        self.add_widget(title)

        shoppingList=("Aceton - för nagellack","Antihistamin","Rhinocort Aqua","Bisolduo","Alsolsprit","Bomullsrondeller","Bittermandelolja","Eucerin","Lactulos","Mjällschampo - fungoral","Skavsårsplåster","Sårskölj","Talgbollar","Tandborstar","Tandpetare","Tulpaner","Tandkräm","Bomullspinnar","Rakgel","Plåster","Bindor - 6 droppar","Bindor - Always natt","Tvål","Flytande tvål","Näsdukar","Servetter","Påsklämmor","Engångstallrikar","Sugrör","Stearinljus - svarta","Stearinljus - vita kron","Värmeljus","Marshaller","Sanitetsstavar","Presso","Skärbrädor","Bunke - rostfri","Äggskivare","Stektermometer","Lökburk","Ved","Grilltång","Grillspett","Grillkol","Tändvätska","Paketsnöre","Presentpapper","Glödlampa","Superlim","Whiteboardpenna","Halogenlampa","Kuvert","A4-papper","AA-batterier","9-voltsbatteri","Toaborste","3-voltsbatteri 2032","Engångsgummihandskar","Avloppsplopp","Soppåsar","Diskborste","Disksvampar","Disktrasor","Skurtrasor","Golvmopp","Undermatta","Plastlåda","Tvättmedel - kulör")#,"Tvättmedel - vit","Tvättmedel - svart","Såpa - grön","Diskmedel - maskin","Diskmedel - hand","Kalkosan","Svinto","Fönsterputs","Kattmynta","Mässingsputs","Kalkborttaging","Toalettrengöring","Bakplåtspapper","Smörgåspapper","Aluminiumfolie","Plastfolie","Pajformar","Tvättpåse","Plastpåsar - 1 liter","Plastpåsar - 3 liter","Plastpåsar - 2 liter","Braständare","Tändstickor","Toapapper","Hushållspapper","Torky","Ramlösa","Sprite","Läsk","Tonic","Julmust","Källvatten","Glögg","Öl - alkoholfri","Pofiber","Kex","Flädersaft","Ostkex","Crustader","Finn crisp","Tunnbröd","Fröknäcke","O'boy","Kaffe","Pukka","Skosnören","Fiberhusk","Pasta - glutenfri","Njalla","Rågkaka - Polar","Lingongrova","Rostbröd","Hamburgerbröd","Korvbröd","Pizzadeg","Srirachamajonäs","Hummus","Kycklinginnerfilé","Kycklingfilé","Kyckling hel","Kycklling - grilad","Parmaskinka","Leverpastej","Ingelstakorv","Grillkorv","Varmkorv","Prinskorv - Ingelsta","Falukorv","Sidfläsk","Skinka - rökt - bit","Bacon","Köttbullar","Västerbotten","Åseda","Chèvre","Halloumi","Parmesanost","Ricotta","Boursin","Brie","Ädelost","Fetaost","Mozzarella - mini","Mozzarella - riven","Mozzarella","Köttfärs","Marinad","Fläskfilé","Fläskkarré","Lammkotletter","Lammfärs","Lammstek","Salami","Skinka - rökt - skivor","Lax","Skagenröra","Tonfisk","Torskrygg","Romsås","Rom","Räkor - färska","Räkor - skalade","Röding - gravad","Musslor - Abbas stora","Gravlaxsås","Hollandaisesås 3dl","Ansjovisfiléer","5-minuterssill","Inläggningssill","Matjessill","Pepparrot på tub","Proviva shots","Philadelphiaost","Jäst för matbröd","Jäst för söta degar","Laktosfri turkisk yoghurt","Grädde","Laktosfri bregott","Laktosfri kvarg","Laktosfri gräddfil","Laktosfri crème fraiche","Laktosfri keso","Kesella 10%","Laktosfri fil","Laktosfri mjölk","Laktosfri yoghurt - 6%","Fil","Mjölk","Smör","Ägg","Hallon - färska","Blåbär - färska","Björnbär - färska","Jordgubbar - svenska","Physalis","Passionsfrukt","Selleristjälk","Persilja - färsk","Dill - färsk","Gräslök","Sparris","Cosmopolitansallad","Spenat","Grönkål","Sallad","Crispsallad","Ruccola","Maché","Citron","Avocado","Gurka","Paprika","Ingefära","Spetspaprika","Lök - färsk","Salladslök","Tomater","Tomater - små","Pärltomater","Chillifrukt","Pimiento de padrone","Purjolök","Fikon","Fänkål","Broccoli","Blomkål","Haricots verts","Sockerärtor","Aubergine","Kantareller","Champinjoner","Portabellasvamp","Zucchini","Kålrot","Kålrabbi","Pepparrot","Morötter","Brysselkål","Rödbetor","Majskolvar","Rotselleri","Palsternacka","Delikatessgurka","Sötpotatis","Vitkål","Rödkål","Pumpa","Äpple","Lime","Frukt","Ananas","Apelsiner","Banan","Clementiner","Druvor","Granatäpple","Grapefrukt","Kiwi","Mango","Melon","Plommon","Päron","Juice","Salvia - färsk","Basilika - färsk","Koriander - färsk","Mynta - färsk","Oregano - färsk","Rosmarin - färsk","Timjan - färsk","Potatis","Charlottenlök","Lök - gul","Lök - röd","Lök - vit","Lök - solo","Steklök","Oliver - gröna","Oliver - svarta","Paprika - grillad","Grönsaksbuljong","Fiskbuljong","Oxbuljong","Kycklingbuljong","Lantbuljong","Ajvar","Harissa","Currypasta - röd","Sambal oelek","Pickles","Kokosmjölk","Senap","Senap - söt och stark","Ketchup","Tomatpuré","Olivolja - fin","Olivolja - billig","Frityrolja","Kokosolja","Soltorkade tomater","Tomater - krossade","Tomater - små hela på burk","Tomater - skalade på burk","Gazpacho","Risvinäger","Rapsolja","Vinäger","Balsamvinäger","Ättika","Soya","Worcestershiresås","Hamburgerdressing (rosa)","Majonäs","Aioli","Tabasco","Sataysås","Pad thai","Fisksås","Tortillas","Fajitaskrydda","Jalapeños på burk","Tacokrydda","Salsa - medium","Basilika - torkad","Brödkryddor - S:ta Maria","Cayennepeppar","Chilliflakes","Chillipulver","Curry","Enbär - torkade","Franska örter - torkade","Kanel - hel","Kanel - mald","Kardemumma - hel","Kardemumma - mald","Koriander - mald","Lökpulver","Mynta - torkad","Nejlikor 50g","Oregano - torkad","Paprikapulver","Rosmarin - torkad","Rosépeppar - hel","Spiskummin - mald","Stjärnanis - hel","Svartpeppar - hel","Svartpeppar - mald","Timjan - torkad","Vitlökspulver","Vitpeppar - hel","Örtagårdskrydda","Salt - fling","Salt - kvarn","Salt","Pesto","Risblad","Nudlar - sötpotatis - Ari Rang","Nudlar","Basmatiris","Grötris","Quinoa","Pasta","Tagliatelle","Spagetti","Citronfrommage","Mullbär - torkade","Aprikoser - torkade","Dadlar","Plommon - torkade","Tranbär - torkade","Russin","Lingonpulver - frystorkat","Chokladask","Lösgodis","Berry boost","Julnötter","Valnötter","Hasselnötter","Cashewnötter","Mandlar","Paranötter","Bittermandel","Mandlar - skalade","Mandelflarn - rostade","Mandelmjöl","Kokoschips","Kokosflingor","Tomatjuice","Bakpulver","Kristyr - vit","Vaniljpulver","Vaniljstång","Gelatinblad","Honung - flytande","Strösocker","Honung - fast","Råsocker","Florsocker","Mandelmassa","Karamellfärg - röd","Choklad - mörk","Choklad - vit","Choklad - ljus","Kakao","Havrepuffar","Jäst - torr","Vetemjöl","Havregryn","Havrekli","Pepparkakshus","Bovetemjöl","Sojamjöl","Rågmjöl","Potatismjöl","Psylliumhusk","Rågflingor","Vallmofrön - blå","Sesamfrön","Solrosfrön","Linfrön","Granola - Paulúns med dadlar och nötter","Pinjenötter","Mango - fryst","Pumpafrön","Jordgubbssylt","Drottningsylt","Ättiksgurka","Marmelad","Cornichoner","Kikärtor","Vita bönor","Jordnötter - saltade","Nötmix","Chips","Dipsås","Popcorn","Gambas - frysta","Räkor - frysta","Laxkuber","MSC vitfisk - fryst","Lax - fryst","Viltskav - fryst","Renskav - fryst","Pommes frites","Gräslök - fryst","Ärtor - frysta","Kycklingbröst - frysta","Kycklingklubbor - frysta","Glass","Jordgubbar - frysta","Ananas - fryst","Hallon och blåbär - frysta","Hallon - frysta","Blåbär - frysta","Non-stop","Choklad","Bon aqua","Tuggummi","Rakblad","Saffran","Schampo","Spotify")

        scrollBox = ScrollView(
            size_hint=(1, .9),
            do_scroll_x=False,
        )
        self.add_widget(scrollBox)

        stack = StackLayout(size_hint=(1, None))
        stack.bind(
            minimum_height=stack.setter('height')
        )
        scrollBox.add_widget(stack)

        for item in shoppingList:
            label = Button(
                    text=item,
                    height=title.height,
                    size_hint=(1, None),
                )
            def callback(instance):
                if instance.background_color == [1,1,1,1]:
                    instance.background_color = [0,0,1,1]
                else:
                    instance.background_color = [1,1,1,1]
                if self.hide.state == 'down':
                    stack.remove_widget(instance)
            label.bind(on_release = callback)
            stack.add_widget(label)

        buttons = BoxLayout(
            size_hint=(1, .05)
        )
        self.add_widget(buttons)
        buttons.add_widget(
            Label(
                text="Hide:",
                size_hint=(None, 1)
            ))
        self.hide = CheckBox(
                size_hint=(None, 1)
            )
        buttons.add_widget(self.hide)
        buttons.add_widget(
            Button(
                text="Quit",
                on_release=exit,
                size_hint=(1, 1)
            ))

class Checker(App):

    def build(self):
        return CheckList()

if __name__ == '__main__':
    Checker().run()


