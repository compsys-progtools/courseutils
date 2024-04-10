from .grade_constants import exp_thresh, community_cost
from .grade_constants import letter_df 
from .grade_constants import bonus_criteria, weights, default_badges


def community_apply(student_dict):
    '''
    take dictionary of badge keys and apply community badges, converting to 
    others if applicable, then return the updated

    Parameters
    ----------
    badges_in : dict
        dictionary with keys as badges/bonuses and counts in values
    '''
    # apply community badges if needed
    if student_dict['experience'] < exp_thresh and student_dict['community']>0:
        experience_needed = exp_thresh - student_dict['experience']
        community_needed = experience_needed*community_cost['experience']
        if student_dict['community'] >=community_needed:
            student_dict['community'] -= community_needed
            student_dict['experience'] += experience_needed

    rp_sum = student_dict['review'] + student_dict['practice']
    if rp_sum <18:
        # doing this lazy instead of a loop
        if student_dict['community'] >= community_cost['practice']:
            student_dict['community'] -= community_cost['practice']
            student_dict['practice'] += 1
        if student_dict['community'] >= community_cost['practice']:
            student_dict['community'] -= community_cost['practice']
            student_dict['practice'] += 1
        if student_dict['community'] >= community_cost['review']:
            student_dict['community'] -= community_cost['review']
            student_dict['review'] += 1
        if student_dict['community'] >= community_cost['review']:
            student_dict['community'] -= community_cost['review']
            student_dict['review'] += 1
        if student_dict['community'] >= community_cost['review']:
            student_dict['community'] -= community_cost['review']
            student_dict['review'] += 1

    return student_dict


def calculate_grade(badges_in,return_influence=False):
    '''
    compute grade from dictionary

    Parameters
    ----------
    badges_in : dict
        dictionary with keys as badges/bonuses and counts in values
    return_influence : bool {False}
        if true, return influence instead of letter
    '''
    current_badges = default_badges.copy()
    current_badges.update(badges_in)
    # apply bonuses 
    current_badges.update({bname:bfunc(current_badges) for bname,bfunc in bonus_criteria.items()})
    # compute final
    influence = sum([current_badges[k]*weights[k] for k in weights.keys()])
    
    letter_grade = letter_df[letter_df['threshold']<=influence].iloc[-1].name.strip()

    if return_influence:
        return influence
    else:
        return letter_grade