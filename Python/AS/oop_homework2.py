import numpy as np
import random
import time


class Test(object):
    def __init__(self, name, points, no_pc):
        self.num_of_professors = 31
        self.num_of_trials = 1000000
        self.name = name
        self.points = points
        self.no_pc = no_pc

    def init(self, nop, no_pc):

        # Create nd_arrays for professors,applicants and professors chosen to vote for somebody.
        a = np.zeros((3, 16), dtype=np.int32)
        no_ip = nop - no_pc
        scores = np.zeros(16, dtype=np.int32)
        return a, scores, no_ip

    def vote(self, a, no_pc, no_ip):
        pass
        # First,professors_chosen vote for specific candidates.
        for ii in range(3):
            a[0, ii] = no_pc
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

    def get_scores_chosen(self, a, soa):

        for t in range(16):
            soa[t] = a[0, t] * self.points[0] + a[1, t] * self.points[1] + a[2, t] * self.points[2]
        scores_sorted = np.argsort(soa)[::-1]
        # if scores_sorted[7] == scores_sorted[8]:
        #     applicants, scores_of_applicants, num_of_impartial_prof = self.init(self.num_of_professors, self.no_pc)
        #     applicants_voted = self.vote(applicants, self.no_pc, num_of_impartial_prof)
        #     chosen_onetime = self.get_scores_chosen(applicants_voted, scores_of_applicants)
        # else:
        #     pass
        chosen_onetime = scores_sorted[:8]

        return chosen_onetime

    def print_results(self):
        chosen1 = np.zeros(17, dtype=np.int32)
        for n in range(self.num_of_trials):
            applicants, scores_of_applicants, num_of_impartial_prof = self.init(self.num_of_professors, self.no_pc)
            applicants_voted = self.vote(applicants, self.no_pc, num_of_impartial_prof)
            chosen_once = self.get_scores_chosen(applicants_voted, scores_of_applicants)
            if 0 in chosen_once and 1 in chosen_once and 2 in chosen_once:
                chosen1[16] += 1
            else:
                pass
            for i in range(8):
                chosen1[chosen_once[i]] += 1

        print(chosen1)
        probabilityT1 = chosen1[0]/self.num_of_trials
        probabilityT2 = chosen1[1]/self.num_of_trials
        probabilityT3 = chosen1[2]/self.num_of_trials
        probabilityT1T2T3 = chosen1[16]/self.num_of_trials

        print(self.name+"(A/B/C=", "5/", self.points[1], "/1points;X=", self.no_pc, ") :",
              "\nT1 funded:", probabilityT1,
              "\nT2 funded:", probabilityT2,
              "\nT3 funded:", probabilityT3,
              "\nT1,T2,T3 all funded:", probabilityT1T2T3)


start = time.process_time()
points1_2 = [5, 3, 1]
points3_4 = [5, 2, 1]
num_of_professors_chosen1_3 = 5
num_of_professors_chosen2_4 = 3


t1 = Test("Test1", points1_2, num_of_professors_chosen1_3)
t1.print_results()
t2 = Test("Test2", points1_2, num_of_professors_chosen2_4)
t2.print_results()
t3 = Test("Test3", points3_4, num_of_professors_chosen1_3)
t3.print_results()
t4 = Test("Test4", points3_4, num_of_professors_chosen2_4)
t4.print_results()
end = time.process_time()
print('Time elapse is %6.3f' % (end - start))

