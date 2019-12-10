from operator import itemgetter

class Cichelli:
    datas = list()
    docs_name = ""
    letter_points = dict()
    hashing_letter_points = dict()
    addresses = list()
    max_increment = 4


    def __init__(self,get_data):
        ## Harf vs farklılıkları için hepsini küçük harfe çevir.
        self.docs_name = get_data.lower()

        ## veriyi sıralamaya gönder
        self.sorting_datas()

        ## hashleyerek adresini ver
        self.hashing_datas()
        print("--------")
        print("Harflerin Geçme Sayısı")
        for key,point in self.letter_points.items():
            print("{} harfi {} kere geçiyor.".format(key,point))

        print("--------")
        print("Kelimelerin Sıralaması")
        count = 1
        for key,point in self.datas:
            print("{}.{} ( Puanı : {} ) ".format(count,key,point))
            count += 1
        print("--------")
        print("Harf Puanları ( Hashing için )")
        for key,data in self.hashing_letter_points.items():
            print("{} : {}".format(key,data[0]))
        print("--------")
        print("Kelimelerin Kayıt Edildiği Adres")
        for key,data in self.addresses:
            print("{} - {}".format(data,key))
        print("***********************")
    ## girilen verinin puanlanması ve yeniden sıralama işlemleri
    def sorting_datas(self):
        ## Toplam karakter sayısı
        h0 = len(self.docs_name)

        ## 1. harfi
        h1 = self.docs_name[0]

        ## son harfi
        h2 = self.docs_name[-1]

        ## Harflerin kaç kere geçtiğini hesaplamak için, sayılarının tutulduğu fonksiyona gönder.
        h1_point = self.add_letter_point(h1)
        h2_point = self.add_letter_point(h2)

        ## Sistemde ekli olanların hepsinin puanlarını güncelliyoruz ( yeni gelen harf için )
        self.data_sort_point(h1_point,h2_point)

    ## ilk sıralama için harflerin kaç kare geçtiğini hesaplayıp , puan ver.
    def add_letter_point(self,letter):

        ## eğer daha önce geçen bir harf ise var olan elemana +1 ekle
        if letter in self.letter_points.keys():
            self.letter_points[letter] += 1
        ## harf sisteme ilk defa geldiyse, harfli listeye ekle.
        else:
            self.letter_points[letter] = 1

        ## çakışma durumunda hashing yaparken harflerin puanlarına bakılacak. Bundan dolayı harflerin puanlarının olduğu
        ## bir dizi tutup, her harfin 1 kere eklenmesini sağlıyoruz. Ayrıca 2. parametre olarak başka veride kullanılıp
        ## kullanılmadığını kontrol ediyoruz.
        if not letter in self.hashing_letter_points.keys():
            self.hashing_letter_points[letter] = [0,0,0]
        return self.letter_points[letter]

    ## eklenen ve eklenecek verinin sıralama puanı ve puana göre sıralanması.
    def data_sort_point(self,h1_point,h2_point):
        self.datas.append([self.docs_name,h1_point + h2_point])
        for key,value in self.datas:
            new_h1_point = self.letter_points[key[0]]
            new_h2_point = self.letter_points[key[-1]]
            list_key = self.datas.index([key,value])
            self.datas[list_key] = [key,new_h1_point + new_h2_point]
        ## verileri en büyük puandan itibaren sıralıyoruz.
        self.datas.sort(key=itemgetter(1), reverse=True)


        ## adreslemeye ekliyoruz
        self.addresses.append([self.docs_name,len(self.docs_name) + self.hashing_letter_points[self.docs_name[0]][0] + self.hashing_letter_points[self.docs_name[-1]][0]])

    def hashing_datas(self,letter = "",increment = 0):
        address_tamp = list()
        if not letter == "":
            self.letter_point_edit(letter,increment)
        count = 0
        for data,address in self.addresses:
            first_letter = data[0]
            last_letter = data[-1]
            if address in address_tamp:
                print("Çakışma : {} (Çakıştığı Adres : {})".format(data, address))
                if (self.hashing_letter_points[first_letter][1] == 0 or self.hashing_letter_points[first_letter][2] == 1):
                    self.hashing_letter_points[first_letter][2] = 1
                    self.hashing_datas(first_letter,1)
                elif (self.hashing_letter_points[last_letter][1] == 0 or self.hashing_letter_points[first_letter][2] == 1):
                    self.hashing_letter_points[last_letter][2] = 1
                    self.hashing_datas(last_letter,1)
                else:
                    print("{} için artırım yapılamıyor".format(data))
                    print("bir önceki veri olan ## {} ## için arttırım yapılacak".format(self.addresses[count - 1]))
            else:
                self.hashing_letter_points[data[0]][1] = 1
                self.hashing_letter_points[data[-1]][1] = 1
                address_tamp.append(address)

            self.hashing_letter_points[first_letter][2] = 0
            self.hashing_letter_points[last_letter][2] = 0
            count += 1

    def letter_point_edit(self,letter,increment):
        if(self.hashing_letter_points[letter][0] == self.max_increment):
            print("Max increment sayısına ulaştı")
        else:
            print("{} harfi için arttırım yapılıyor.".format(letter))
            self.hashing_letter_points[letter][0] += increment
            self.hashing_letter_points[letter][1] += increment
            self.hashing_point_update()
            print("{} harfinin yeni puanı : {}".format(letter,self.hashing_letter_points[letter][0]))

    def hashing_point_update(self):
        self.addresses.clear()
        for data,key in self.datas:
            self.addresses.append([data,len(data) + self.hashing_letter_points[data[0]][0] + self.hashing_letter_points[data[-1]][0]])


while True:
    print("Bir Kelime Giriniz ( Çıkmak için -1 yazınız ) ")
    add_data = input()
    if add_data == "-1":
        break
    else:
        Cichelli(add_data)

