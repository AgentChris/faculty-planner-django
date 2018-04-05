import difflib
from fuzzywuzzy import fuzz

name_personal = 'Cristi Poputea'  # facebook
name_school = 'POPUTEA CRISTIAN DANIEL'  # faculty

names = """Irwin Carrero  
Chanelle Argo  
Somer Bonaparte  
Deetta Pouliot  
Roosevelt Hu  
POPUTEA CRISTIAN DANIEL
Idella Calderon  
Ginger Jerrell  
Bernadine Sprvill  
Christal Schwandt  
Noemi Calcagni  
Chaya Gillette  
POPU'I‘EA D CRISTIANVDANIEL
Tonia Endsley  
Ewa Whisenant  
Sandie Schillinger  
Frankie Propp  
Leah Rolfe  
Tamie Bevill  
Concetta Hendrixson  
Dewitt Crose  
Shera Robichaud  
Darnell Vincent  
Precious Easter  
Mao Helton  
Micheline Borger  
Jess Walkes  
Young Leadbetter  
Josh Rufener  
Esperanza Arends  
Alonzo Rohlfing  
Jana Blackwelder  
Margarita Hobgood  
Tiffany Andes  
Ouida Stclaire  
Marcos Knisely  
Verna Patin  
Juliann Olivieri  
Trudi Delorme  
Thad Reineck  
Edda Jeans  
Letty Biles  
Katy Sisler  
Shantelle Mcdougal  
Maurita Fawcett  
Junior Borth  
Keiko Hartline  
Jung Fugitt  
Mildred Vosburgh  
Valentine Schuck  
Patria Mckinney  
Marcelle Sequeira  
Kim Alessi  
Cornell Marth  
Modesta Moffat  
Chara Toupin  
Hellen Dutremble  
Taneka Huntsberry  
Palmira Laverdiere  
Lorie Oneal  
Katherin Munger  
Misha Bains  
Azalee Heckert  
Donna Crist  
Eboni Britain  
Allyn Etter  
Yuonne Stanberry  
Vannesa Hao  
Terina Demuth  
Christi Grimes  
Raguel Melendez  
Krystle Hydrick  
Roslyn Shippee  
Edris Giebler  
Ismael Whited  
Thuy Wiltshire  
Natasha Coard  
Trisha Tandy  
Hettie Steyer  
Evelia Spenser  
Kyle Winford  
Nakia Mccusker  
Forest Bramer  
Miles Giunta  
William Fesler  
Collin Range  
Larae Luedke  
Cedric Deboer  
Aisha Ayres  
Magaly Mcquarrie  
Alda Permenter  
Daniell Shih  
Elvina Cron  
Nilda Uhl  
Lawana Pelto  
Scott Quayle  
Alline Munden  
Oren Mctaggart  
Lincoln Vitti  
Katrina Bast  
Brain Pingree  
Ermelinda Minardi  
Kayce Heyman  
Phyllis Mcquinn  
Classie Marano  
Brendan Bonar  
Talia Yahn  
Zachariah Fauntleroy  
Earlene Pazos  
Jeannetta Dane  
Sonya Heiser  
Eleonora Fedrick  
Deadra Bauder  
Laurine Ramer  
Jarod Milliman  
Carolann Winrow  
Carmella Baumert  
Jeanetta Schiff  
Ermelinda Holman  
Elise Ansell  
Wendell Tabron  
Frederica Everton  
Marine Zazueta  
Myrta Bagwell  
Ethelyn Walk  
Salvatore Bibbs  
Emiko Forbush  
Malia Buskey  
Corinne Kral  
Fidelia Levering  
Myron Sharer  
Maxine Camilleri  
Era Clawson  
Lacey Wineinger  
Brunilda Burruel  
Rayna Reddington  
Marilu Cypert  
Arnulfo Moser  
Madeleine Cogdill  
Racquel Chia  
Katrice Minton  
Edward Beckham  
Bernie Heckler  
Chana Escoto  
Loreta Banh  
Hermina Finkbeiner  
Cami Glanz  
Rebbeca Grainger  
Irmgard Henke  
Erlene Dandy  
Rico Bessette  
Alfredo Valenzula  
Justina Barkley  
Nichelle Monte  
Ilse Dao  
Karrie Reimers  
Olimpia Boling  
Christiana Hocking  
Alva Giancola  
Marhta Ruffo  
Candelaria Wedderburn  
Eustolia Kirker  
Eleanore Gholston  
Joye Resh  
Kory Moman  
Shirlene Markowski  
Latesha Musser  
Lorena Llanas  
Debby Urrutia  
Lidia Whisenhunt  
Daren Molander  
Lois Slinkard  
Dierdre Hagy  
Joline Merrihew  
Deann Hild  
Luigi Mitcham  
Pamala Himes  
Phuong Towle  
Linh Luthy  
Mickie Mays  
Bart Henriksen  
Rashida Marchan  
Sheila Heywood  
Kasie Allmond  
Tawny Dexter  
Glenn Tienda  
Seymour Nadler  
Enoch Killeen  
Julienne Felter  
Jame Hains  
Cleora Fallen  
Nathalie Arambula  
Odell Batts  
Mckenzie Copley  
Conchita Bartel  
Isiah Constable  
Britney Allums  
Rae Maisonet  
Kacey Fann  
Jennefer Lu  
Leeanna Bay  
Genia Pinegar  
Belkis Ketcham  
Dovie Goguen  
Alissa Slane  
Deloise Ursery  
Faviola Slape  
Ronnie Arrellano  
Maia Murrah  
Annabel Vinci  
Shawnna Chacon  
Yessenia Truss  
Elroy Hedgepeth  
Carlee Glatz  
Rhiannon Derbyshire  
Rochel Dargan  
Shanita Lords  
Callie Bosket  
Treena Agustin  
Talisha Chevere  
Micheline Spino  
Adriene Counce  
Prince Cann  
Rosia Gatto  
Scarlet Haddox  
Teodoro Falbo  
Dinorah Bourland  
Luvenia Vanhorn  
Charlotte Segars  
Ike Eckles  
Clare Touchton  
Tianna Ayres  
Carman Whitchurch  
Mirella Purser  
Amos Tam  
Israel Massey  
Lawanna Womer  
Tandy Licon  
Carlyn Westman  
Pricilla Juhl  
Leslee Lambros  
Ana Stevenson  
Halley Parmer  
Rosena Lockman  
Noma Morton  
Geri Calderone  
Kitty Ng  
Lorri Ettinger  
Katherine Barley  
Venus Gerrard  
Zenaida Parrett  
Pia Pipkin  
"""

if __name__ == '__main__':
    # name_lower = name.lower()
    # name_school_lower = name_school.lower()

    # name_tokens = list(map(str.lower(), name.split()))
    # name_school_tokens = list(map(str.lower(), name_school.split()))

    ratios = []
    for name in names.split('\n'):
        ratio = fuzz.token_set_ratio(name_personal, name.strip())
        print(f'Ratio fuzzy: {ratio}')
        ratios.append((ratio, name.strip()))

    ratios_sorted = sorted(ratios, key=lambda e: e[0], reverse=True)
    print(ratios_sorted)
    # print(name_lower)
    # print(name_school_lower)
    # matcher = difflib.SequenceMatcher(a=name_lower, b=name_school_lower)
    # matcher.ratio()

    # print(f'Ratio: {matcher.ratio()}')

