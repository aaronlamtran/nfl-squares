class WLine:
    def __init__(self, quarter_scores):
        self.quarter_scores = quarter_scores
        self.check_input_edge_cases()
        self.chunk_length = 10
        self.concatenated_score_line = ''
        self.make_score_string()
        self.add_zeros_for_no_OT()
        self.add_hyphens()
        self.calc_quarter_totals()

    def check_input_edge_cases(self):
        if not self.quarter_scores or self.quarter_scores == '-,-,-,-':
            self.quarter_scores = '0,0,0,0'
        if '-' in self.quarter_scores:
            self.quarter_scores = self.quarter_scores.replace('-', '0')
        # if len(self.quarter_scores.split(',')) < 4:


    def make_score_string(self):
        quarters = self.quarter_scores.split(',')

        for i in range(len(quarters)):
            if len(quarters[i]) == 1:
                quarters[i] = ''.join(('0', quarters[i]))

        self.quarter_scores = ''.join(quarters)

    def add_zeros_for_no_OT(self):
        if len(self.quarter_scores) < self.chunk_length:
            self.quarter_scores = ''.join(
                (self.quarter_scores, "00"))

    def add_hyphens(self):
        hyphens = '-' * 10
        self.concatenated_score_line = self.quarter_scores + hyphens

    def calc_quarter_totals(self):

        q1 = int(self.concatenated_score_line[:2])
        q2 = int(self.concatenated_score_line[2:4])
        q3 = int(self.concatenated_score_line[4:6])
        q4 = int(self.concatenated_score_line[6:8])
        ot = int(self.concatenated_score_line[8:10])

        pos1 = str(q1)
        pos2 = str(q1 + q2)
        pos3 = str(q1 + q2 + q3)
        pos4 = str(q1 + q2 + q3 + q4)
        pos5 = str(q1 + q2 + q3 + q4 + ot)

        self.quarter_scores = pos1 + ',' + pos2 + ',' + pos3 + ',' + pos4 + ',' + pos5

        self.make_score_string()

        self.concatenated_score_line = self.concatenated_score_line + self.quarter_scores

    def get_line(self):
        return self.concatenated_score_line


