from data_prep import load_files, about_q, parse_categories

class WVS_Data:
    
    def __init__(self, responses_file='data/wvs_data.csv',
                 codebook_file='data/F00003861-WV6_Codebook_v_2014_11_07.xls'):
        self.responses, self.codebook = load_files(responses_file, codebook_file)
    
    def __repr__(self):
        return ('Responses: {}\n'
                'Codebook: {}'.format(self.responses.shape, self.codebook.shape))
        
    def about_q(self, var):
        about_q(self.codebook, var)
        
    def parse_categories(self, var):
        parse_categories(self.codebook, var)