"""
PROBLEM:
16 applicants,8 quotas,31 professors,everyone has 3A,3B and 3C.
However,5 professors intend to vote 3A for some specific candidates.
Other ballots are  distributed randomly.
A:5points,B:3points,C:1points.Then Teachers with the top 8 comprehensive scores
can receive fund support.
Number of trials is set on 10,000.
"""

import random
import numpy as np
import time


def init(nop, no_pc):
    pass
    # Create nd_arrays for professors,applicants and professors chosen to vote for somebody.
    # professors = np.ones((3, nop), dtype=np.int32)
    # professors *= 3
    a = np.zeros((3, 16), dtype=np.int32)
    no_ip = nop - no_pc
    # professors_chosen = np.ones((3, nopc), dtype=np.int32)
    scores = np.zeros(16, dtype=np.int32)
    return a, scores, no_ip


def vote(a, no_pc, no_ip):
    pass
    # First,professors_chosen vote for specific candidates.
    for mm in range(3):
        a[0, mm] = no_pc
    # randomly choose 9 ballots from[1,16] each professor.
    # 26 impartial professor vote
    for num in range(no_ip):
        matrix_vote_26 = np.array(random.sample(range(16), 9)).reshape(3, 3)
        for ii in range(3):
            for jj in range(3):
                a[ii, matrix_vote_26[ii, jj]] += 1
    # 5 special professors vote
    for num in range(no_pc):
        matrix_vote_5 = np.array(random.sample(range(3, 16), 6)).reshape(2, 3)
        for ii in range(2):
            for jj in range(3):
                # skip first row,that's the A row.
                a[ii+1, matrix_vote_5[ii, jj]] += 1

    return a


def get_scores_chosen(a, soa, p):

    for t in range(16):
        soa[t] = a[0, t] * p[0] + a[1, t] * p[1] + a[2, t] * p[2]
    scores_sorted = np.argsort(soa)[::-1]
    chosen_onetime = scores_sorted[:8]

    return chosen_onetime


start = time.process_time()

points1_2 = [5, 3, 1]
points3_4 = [5, 2, 1]
num_of_professors = 31
num_of_applicants = 16
num_of_professors_chosen1_3 = 5
num_of_professors_chosen2_4 = 3
num_of_trials = 100000

# Test1
chosen1 = np.zeros(17, dtype=np.int32)
for n in range(num_of_trials):
    applicants, scores_of_applicants, num_of_impartial_Prof = init(num_of_professors, num_of_professors_chosen1_3)
    applicants_voted = vote(applicants, num_of_professors_chosen1_3, num_of_impartial_Prof)
    chosen_once = get_scores_chosen(applicants_voted, scores_of_applicants, points1_2)
    if 0 in chosen_once and 1 in chosen_once and 2 in chosen_once:
        chosen1[16] += 1
    else:
        pass
    for i in range(8):
        chosen1[chosen_once[i]] += 1

print(chosen1)
probabilityT1 = chosen1[0]/num_of_trials
probabilityT2 = chosen1[1]/num_of_trials
probabilityT3 = chosen1[2]/num_of_trials
probabilityT1T2T3 = chosen1[16]/num_of_trials

print("Test1 (A/B/C=5/3/1points;X=5) :",
      "\nT1 funded:", probabilityT1,
      "\nT2 funded:", probabilityT2,
      "\nT3 funded:", probabilityT3,
      "\nT1,T2,T3 all funded:", probabilityT1T2T3)

# Test2
# chosen1 = np.zeros(17, dtype=np.int32)
# for n in range(num_of_trials):
#     applicants, scores_of_applicants, num_of_impartial_Prof = init(num_of_professors, num_of_professors_chosen2_4)
#     applicants_voted = vote(applicants, num_of_professors_chosen2_4, num_of_impartial_Prof)
#     chosen_once = get_scores_chosen(applicants, scores_of_applicants, points1_2)
#     if 0 in chosen_once and 1 in chosen_once and 2 in chosen_once:
#         chosen1[16] += 1
#     else:
#         pass
#     for i in range(8):
#         chosen1[chosen_once[i]] += 1
#
# print(chosen1)
# probabilityT1 = chosen1[0]/num_of_trials
# probabilityT2 = chosen1[1]/num_of_trials
# probabilityT3 = chosen1[2]/num_of_trials
# probabilityT1T2T3 = chosen1[16]/num_of_trials
#
# print("Test2 (A/B/C=5/3/1points;X=3) :",
#       "\nT1 funded:", probabilityT1,
#       "\nT2 funded:", probabilityT2,
#       "\nT3 funded:", probabilityT3,
#       "\nT1,T2,T3 all funded:", probabilityT1T2T3)
#
# # Test3
# chosen1 = np.zeros(17, dtype=np.int32)
# for n in range(num_of_trials):
#     applicants, scores_of_applicants, num_of_impartial_Prof = init(num_of_professors, num_of_professors_chosen1_3)
#     applicants_voted = vote(applicants, num_of_professors_chosen1_3, num_of_impartial_Prof)
#     chosen_once = get_scores_chosen(applicants, scores_of_applicants, points3_4)
#     if 0 in chosen_once and 1 in chosen_once and 2 in chosen_once:
#         chosen1[16] += 1
#     else:
#         pass
#     for i in range(8):
#         chosen1[chosen_once[i]] += 1
#
# print(chosen1)
# probabilityT1 = chosen1[0]/num_of_trials
# probabilityT2 = chosen1[1]/num_of_trials
# probabilityT3 = chosen1[2]/num_of_trials
# probabilityT1T2T3 = chosen1[16]/num_of_trials
#
# print("Test3 (A/B/C=5/2/1points;X=5) :",
#       "\nT1 funded:", probabilityT1,
#       "\nT2 funded:", probabilityT2,
#       "\nT3 funded:", probabilityT3,
#       "\nT1,T2,T3 all funded:", probabilityT1T2T3)
#
# # Test4
# chosen1 = np.zeros(17, dtype=np.int32)
# for n in range(num_of_trials):
#     applicants, scores_of_applicants, num_of_impartial_Prof = init(num_of_professors, num_of_professors_chosen2_4)
#     applicants_voted = vote(applicants, num_of_professors_chosen2_4, num_of_impartial_Prof)
#     chosen_once = get_scores_chosen(applicants, scores_of_applicants, points3_4)
#     if 0 in chosen_once and 1 in chosen_once and 2 in chosen_once:
#         chosen1[16] += 1
#     else:
#         pass
#     for i in range(8):
#         chosen1[chosen_once[i]] += 1
#
# print(chosen1)
# probabilityT1 = chosen1[0]/num_of_trials
# probabilityT2 = chosen1[1]/num_of_trials
# probabilityT3 = chosen1[2]/num_of_trials
# probabilityT1T2T3 = chosen1[16]/num_of_trials
#
# print("Test4 (A/B/C=5/2/1points;X=3) :",
#       "\nT1 funded:", probabilityT1,
#       "\nT2 funded:", probabilityT2,
#       "\nT3 funded:", probabilityT3,
#       "\nT1,T2,T3 all funded:", probabilityT1T2T3)

end = time.process_time()
print('Time elapse is %6.3f' % (end - start))
