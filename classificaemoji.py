# -*- Mode: Python; coding: utf-8 -*-

import os, csv
import sys, regex, emoji, re

dic = {':angry_face:':'negativo',
':anxious_face_with_sweat:':'negativo',
':automobile:':'neutro',
':baby_light_skin_tone:':'neutro',
':backhand_index_pointing_down:':'neutro',
':backhand_index_pointing_down_light_skin_tone:':'neutro',
':backhand_index_pointing_down_medium-dark_skin_tone:':'neutro',
':backhand_index_pointing_down_medium-light_skin_tone:':'neutro',
':backhand_index_pointing_down_medium_skin_tone:':'neutro',
':backhand_index_pointing_up_light_skin_tone:':'neutro',
':backhand_index_pointing_up_medium-dark_skin_tone:':'neutro',
':backhand_index_pointing_up_medium_skin_tone:':'neutro',
':baguette_bread:':'neutro',
':balloon:':'neutro',
':beaming_face_with_smiling_eyes:':'positivo',
':beating_heart:':'positivo',
':bottle_with_popping_cork:':'positivo',
':bouquet:':'positivo',
':bride_with_veil_medium-light_skin_tone:':'neutro',
':broken_heart:':'negativo',
':call_me_hand_light_skin_tone:':'positivo',
':chicken:':'neutro',
':clapping_hands:':'positivo',
':clapping_hands_light_skin_tone:':'positivo',
':clapping_hands_medium-light_skin_tone:':'positivo',
':clinking_glasses:':'positivo',
':confetti_ball:':'positivo',
':confused_face:':'neutro',
':confounded_face:':'negativo',
':cross_mark:':'neutro',
':dollar_banknote:':'neutro',
':double_exclamation_mark:':'neutro',
':drooling_face:':'neutro',
':ear_of_corn:':'neutro',
':eye:':'neutro',
':eyes:':'neutro',
':face_blowing_a_kiss:':'positivo',
':face_vomiting:':'negativo',
':face_with_open_mouth:':'neutro',
':face_with_tears_of_joy:':'positivo',
':face_with_tongue:':'neutro',
':face_savoring_food:':'neutro',
':face_screaming_in_fear:':'neuto',
':fire:':'neutro',
':folded_hands_medium_skin_tone:':'positivo',
':folded_hands_light_skin_tone:':'positivo',
':footprints:':'neutro',
':frowning_face:':'negativo',
':ghost:':'neutro',
':giraffe:':'neutro',
':grimacing_face:':'negativo',
':grinning_cat_face:':'neutro',
':grinning_face:':'positivo',
':grinning_face_with_smiling_eyes:':'positivo',
':grinning_face_with_big_eyes:':'positivo',
':hot_beverage:':'neutro',
':house_with_garden:':'neutro',
':index_pointing_up:':'neutro',
':index_pointing_up_medium_skin_tone:':'neutro',
':index_pointing_up_medium-light_skin_tone:':'neutro',
':kissing_face:':'positivo',
':kissing_face_with_smiling_eyes:':'positivo',
':loudspeaker:':'neutro',
':loudly_crying_face:':'negativo',
':magnifying_glass_tilted_left:':'neutro',
':man:‍':'neutro',
':man_dancing_medium_skin_tone:':'neutro',
':meat_on_bone:':'neutro',
':motor_scooter:':'neutro',
':nauseated_face:':'negativo',
':NEW_button:':'neutro',
':no_entry:':'neutro',
':octopus:':'neutro',
':oncoming_automobile:':'neutro',
':oncoming_fist:':'positivo',
':oncoming_fist_medium-light_skin_tone:':'positivo',
':oncoming_fist_medium_skin_tone:':'positivo',
':peanuts:':'neutro',
':person_biking:‍':'neutro',
':person_biking_light_skin_tone:‍':'neutro',
':person_facepalming_medium-dark_skin_tone:‍':'negativo',
':person_gesturing_OK_medium_skin_tone:‍':'neutro',
':person_raising_hand:‍':'neutro',
':person_raising_hand_medium_skin_tone:\u200d':'neutro',
':person_raising_hand_medium_skin_tone:':'neutro',
':person_raising_hand_light_skin_tone:‍':'neutro',
':person_raising_hand_medium_skin_tone:':'neutro',
':person_running:‍':'neutro',
':person_running_medium_skin_tone:‍':'neutro',
':person_shrugging_medium_skin_tone:\u200d':'neutro',
':pile_of_poo:':'negativo',
':pill:':'neutro',
':police_car:':'neutro',
':popcorn:':'neutro',
':poultry_leg:':'neutro',
':raised_fist_medium-light_skin_tone:':'neutro',
':raising_hands:':'neutro',
':raising_hands_medium_skin_tone:':'neutro',
':red_heart:':'positivo',
':revolving_hearts:':'positivo',
':rolling_on_the_floor_laughing:':'positivo',
':rooster:':'neutro',
':sad_but_relieved_face:':'negativo',
':scissors:':'neutro',
':selfie:':'neutro',
':see-no-evil_monkey:':'neutro',
':sleepy_face:':'negativo',
':slightly_frowning_face:':'neutro',
':slightly_smiling_face:':'positivo',
':small_airplane:':'neutro',
':smiling_face_with_halo:':'neutro',
':smiling_face_with_heart-eyes:':'postivo',
':smiling_face_with_horns:':'negativo',
':sparkling_heart:':'positivo',
':speaker_high_volume:':'neutro',
':sun:':'neutro',
':sunflower:':'positivo',
':sun_behind_large_cloud:':'neutro',
':syringe:':'neutro',
':thumbs_up:':'neutro',
':thumbs_up_light_skin_tone:':'positivo',
':thumbs_up_medium-dark_skin_tone:':'positivo',
':thumbs_up_medium_skin_tone:':'positivo',
':TOP_arrow:':'neutro',
':tropical_fish:':'neutro',
':unamused_face:':'neuto',
':victory_hand_light_skin_tone:':'positivo',
':volleyball:':'neutro',
':waving_hand_light_skin_tone:':'neutro',
':waving_hand_medium-light_skin_tone:':'neutro',
':white_heavy_check_mark:':'neutro',
':winking_face:':'positivo',
':winking_face_with_tongue:':'neutro',
':woman_dancing_light_skin_tone:':'neutro',
':wrapped_gift:':'positivo'}


def split_count(text):

    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list

#Diretorio onde se encontra o arquivo com conversas so Whatsapp
ARQ = (r'C:\Users\leonardo\Desktop\grupo.txt')

cont = 0
#Inicia leitura do arquivo
with open(ARQ, 'r', encoding='utf8', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=':', quotechar='\n')
    for line in reader:
        try:
            #a = (extract_emojis(line[2]))
            counter = split_count(line[2])
            a = ' '.join(emoji for emoji in counter)
        except:
            pass
        b = len(a)
        #print(b)
        if b > 0:
            lista = a.split()
            classe = emoji.demojize(lista[0])
            cont = cont + 1
            try:
                print(line[2],";",dic[classe])
         
            #try:
                #linha = line[2]
            except:
                pass  
            #print("##",cont,linha,";",dic[classe])
            #except:
                #pass
            
csvfile.close()
