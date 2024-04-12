import pandas as pd

exp_thresh = 22
rp_thresh =18
learning_weights = {'experience' :2, 'lab': 2, 'review': 3,'practice': 6,'explore': 9,'build' :36}
community_weights = {'experience_replace' :3,  'review_replace': 4,'practice_replace': 7, 'review_upgrade': 3,}
bonus_participation = 18
bonus_lab = 18
bonus_breadth = 32
bonus_early = 9

default_badges = {'experience' :0, 
                  'lab': 0, 
                  'review': 0,
                  'practice': 0,
                   'explore': 0,
                   'build' :0,
                 'community': 0,
                 'hack':0,
                 'unstuck': 0,
                 'descriptive': 0,
                 'early': 0,
                  'question':10 }

bonus_criteria = {'participation_bonus': lambda r: int(r['experience'] >=exp_thresh),
                  'lab_bonus':  lambda r: int(r['lab'] >=13),
                   'breadth_bonus': lambda r: int(r['review'] + r['practice']>=rp_thresh),
                 'community_bonus': lambda r: int(r['community']>=10),
                 'unstuck_bonus': lambda r: r['unstuck'],
                 'descriptive_bonus': lambda r: r['descriptive'],
                 'early_bonus': lambda r: r['early'] ,
                 'hack_bonus': lambda r: r['hack'] ,
                 'curiosity_bonus': lambda r: r['question']>10}
bonus_values = {'participation_bonus': bonus_participation,
                  'lab_bonus':  bonus_lab,
                   'breadth_bonus': bonus_breadth,
                 'community_bonus': 18,
                 'hack_bonus':18,
                 'unstuck_bonus': 9,
                 'descriptive_bonus': 9,
                 'early_bonus': 9 ,
                 'curiosity_bonus': 9 }
weights = learning_weights.copy()
weights.update(bonus_values)
community_cost = {'experience':3,
                 'review':4,
                 'practice':7,
                 'review_upgrade':3}

learning_df = pd.Series(learning_weights,name ='complexity').reset_index()
learning_df['badge_type'] = 'learning'

# nans are for learning badges which all ahve weight 1
influence_df = pd.concat([learning_df]).fillna(1).rename(columns={'index':'badge'})
# final df


# base grade influence cutoffs
thresh_mrw = {'F':0,
              'D ':22*learning_weights['experience']+13*learning_weights['lab']+bonus_participation + bonus_lab, 
              'D+':22*learning_weights['experience']+13*learning_weights['lab']+bonus_participation + bonus_lab + 6*learning_weights['review'], 
              'C-':22*learning_weights['experience']+13*learning_weights['lab']+bonus_participation + bonus_lab + 12*learning_weights['review'], 
          'C ':22*learning_weights['experience']+13*learning_weights['lab']+18*learning_weights['review']+\
              bonus_participation + bonus_lab + bonus_breadth,
          'C+':22*learning_weights['experience']+13*learning_weights['lab']+bonus_participation + bonus_lab + bonus_breadth + 6*learning_weights['practice'] + 12*learning_weights['review'], 
          'B-':22*learning_weights['experience']+13*learning_weights['lab']+bonus_participation + bonus_lab + bonus_breadth + 6*learning_weights['review'] + 12*learning_weights['practice'], 
          'B ':22*learning_weights['experience']+13*learning_weights['lab']+18*learning_weights['practice']+\
              bonus_participation + bonus_lab + bonus_breadth,
          'B+': 22*learning_weights['experience']+13*learning_weights['lab'] +18*learning_weights['practice'] +\
              2*learning_weights['explore'] +bonus_participation + bonus_lab + bonus_breadth,
          'A-': 22*learning_weights['experience']+13*learning_weights['lab'] +18*learning_weights['practice'] +\
              4*learning_weights['explore'] +bonus_participation + bonus_lab + bonus_breadth,
          'A ': 22*learning_weights['experience']+13*learning_weights['lab'] +18*learning_weights['practice'] +\
              6*learning_weights['explore'] +bonus_participation + bonus_lab + bonus_breadth}

th_list = [[k,v] for k,v in thresh_mrw.items()]
letter_df = pd.DataFrame(th_list, columns = ['letter','threshold']).sort_values(by='threshold').set_index('letter')
