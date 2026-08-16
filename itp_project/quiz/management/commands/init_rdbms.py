
from django.core.management.base import BaseCommand, CommandError
from quiz.models.rdbms_models import QuizModel

class Command(BaseCommand):
    help = "DB mstr insert script"

    def handle(self, *args, **options):
        self.insertdata();           
        self.stdout.write(
                self.style.SUCCESS("Successfully inserted quiz data")
            )

    def insertdata(self):
        qlist=[]
        qlist.append(QuizModel(23, 'IP', '2013_Oct', 'bacbcdddbbccbacabbbacbcdddcddcbdbcbcbcbbdbdbdacccbccdbccbabbcdcdcadacccdddbcdbbcbccbbcdcacccbcbdccda', '2013A_IP_Question__2013_Oct', 100, 'efmt', 'IP_2013_Oct'));
        qlist.append(QuizModel(27, 'IP', '2014_Oct', 'bbdccadcdcdaacbcccbbdccbcabddddabacbbdcbbddcbaabcacbccbadbcbbcccacaaabbabbcbacbbacbdaacabcdbcdcacdbb', '2014Oct_IP_Question__2014_Oct', 100, 'efmt', 'IP_2014_Oct'));
        qlist.append(QuizModel(28, 'IP', '2015_May', 'dcbbcbbaacacdcddcaabbabdcbaacbdaaccabdbaaabaaababdadbaaabddccbdaccaaacdacadbcdadccbdcdaddadcbcaaaaca', '2015May_IP_Question__2015_May', 100, 'efmt', 'IP_2015_May'));
        qlist.append(QuizModel(31, 'IP', '2015_Oct', 'baccdadbabaadddbadcbbdcbaaccccdbdbddcbabdabaaccbcdbddababcdbdbaaddaabcccddbcbbcabbcbddbbdbcbcacbbbdc', '2015A_IP_Question__2015_Oct', 100, 'efmt', 'IP_2015_Oct'));
        qlist.append(QuizModel(33, 'IP', '2016_Apr', 'aadcbcdbaacacbcbacbbdbddcabbcccbdadbddbcdacabddcbccccbdabdbcbbdbaaddbaccccacbdbdcbbcbbdccdbacdacbdca', '2016S_IP_Question__2016_Apr', 100, 'efmt', 'IP_2016_Apr'));
        qlist.append(QuizModel(35, 'IP', '2016_Oct', 'cacbacdbabbaacbbbcaccdcdcccdacaccbacdbcbccaaadacadbbbbaccacbbbdaccbdadadbdcbcabdbcccaacdccbdbdbbdcbb', '2016A_IP_Question__2016_Oct', 100, 'efmt', 'IP_2016_Oct'));
        qlist.append(QuizModel(24, 'IP', '2014_Apr', 'cadabbddbbdddaabcccaadccbccccdaabbdcccaadaabcaabbbbdaadbbbaacdcbbcdbadcbabcbdbadbcbcabbdcbbacbdbadcd', '2014S_IP_Question__2014_Apr', 100, 'efmt', 'IP_2014_Apr'));
        qlist.append(QuizModel(32, 'FE', '2016_Apr', 'ddddbaddabccdcbdcbdcabddbaddbbdaacdbaacaabdcdadbabdaadddcabbcbbabcdbcbbbaabbbbbc', '2016S_FE_AM-Question__2016_Apr', 80, 'c', 'FE_2016_Apr'));
        qlist.append(QuizModel(2, 'FE', '2007_Apr', 'dcbdbcbbcacbcccababcbcdbbbcbabcdbcdcacbcdcadaabcdbacacbaadadddaaaabbdbcdddccadcc', '2007Apr_FE_AM_Questions__2007_Apr', 80, 'c', 'FE_2007_Apr'));
        qlist.append(QuizModel(3, 'FE', '2007_Oct', 'ccbddbcdccbdcbcacdbdbbcdbabdbdccabaabcbcdbdbacacccbcdababacccddddbbdbbccaddbccbc', '2007Oct_FE_AM_Questions__2007_Oct', 80, 'c', 'FE_2007_Oct'));
        qlist.append(QuizModel(4, 'FE', '2008_Apr', 'abcdcdbbcdcbbdbbdbddddddadbdccacacaddccbbbdddbdddbdddbbdcbbcbaabccbaadcdbccbcbdc', '2008Apr_FE_AM_Questions__2008_Apr', 80, 'c', 'FE_2008_Apr'));
        qlist.append(QuizModel(5, 'FE', '2008_Oct', 'ccaccaddaddcbcddbbccbdbcdbdcccbabbddadddcdcbcaadacadaccdbaabcabbaccbbddddcbccaac', '2008Oct_FE_AM_Questions__2008_Oct', 80, 'c', 'FE_2008_Oct'));
        qlist.append(QuizModel(6, 'FE', '2009_Apr', 'bdbcbdadbacbdcccdbdcbdcdaacccdcbcdaddbabadcbcdbcaddaabdddcacabbcbcaccadaccaabbda', '2009Apr_FE_AM_Questions__2009_Apr', 80, 'c', 'FE_2009_Apr'));
        qlist.append(QuizModel(7, 'FE', '2009_Oct', 'bbbdbbcdbbdaadbcbcccdbcacddddbaaacdcacccadbccabddcabbcdabbdadbaddacaacdaacddaabb', '2009Oct_FE_AM_Questions__2009_Oct', 80, 'c', 'FE_2009_Oct'));
        qlist.append(QuizModel(8, 'FE', '2010_Apr', 'ccbbccccbddbbcacaaabdbbccbaacdacadacbdbdcbbbbbddadcdadcaccadbcdaaacdabbcdacdcbbd', '2010Apr_FE_AM_Questions__2010_Apr', 80, 'c', 'FE_2010_Apr'));
        qlist.append(QuizModel(9, 'IP', '2010_Apr', 'acacdcbbdacadadcdacdbbbbbcbccabbbddbbcacbdccdaddbdbcbcccacdddcdabccdbbdcabbbbaddacaddcdbdbaaacdadabc', '2010S_IP_Questions__2010_Apr', 102, 'e', 'IP_2010_Apr'));
        qlist.append(QuizModel(10, 'FE', '2010_Oct', 'ccacdbcacdccbddadcbccbddaccbcacabddbddabbbacbcdbabdaccbcbbccdbacaccaaddbcbbddbad', '2010Oct_FE_AM_Questions__2010_Oct', 80, 'c', 'FE_2010_Oct'));
        qlist.append(QuizModel(11, 'IP', '2010_Oct', 'aacdabcccacdbccbccadbabbdddcbabdccbbccdacccccdddbadddabdbbccacdbddbcbabcbdabdbcbbddccbdbcbcbbcaaccbc', '2010A_IP_Questions__2010_Oct', 101, 'e', 'IP_2010_Oct'));
        qlist.append(QuizModel(12, 'FE', '2011_Apr', 'bcccddbdcaddbdacaabacdadbbdbcaccbbaadcccdadcdacbbcadbbbabcbcaabadbcbddaccdbadbba', '2011S_FE_AM_Questions__2011_Apr', 80, 'c', 'FE_2011_Apr'));
        qlist.append(QuizModel(13, 'IP', '2011_Apr', 'babdabacadbbcabaccdbbbadbcbccbdcdbdaacaaccbdcdaaccbbcccccdddccdccdbdbaaadccdadadcdcdadccbacbbaacacbd', '2011S_IP_Questions__2011_Apr', 103, 'e', 'IP_2011_Apr'));
        qlist.append(QuizModel(14, 'FE', '2011_Oct', 'cbcccbbcddacccdadbcccbccbcdadaddbcbdaddbcacdbabdbacbacdddbabcbcbbbccacbdabaccccb', '2011A_FE_AM_Question__2011_Oct', 80, 'c', 'FE_2011_Oct'));
        qlist.append(QuizModel(15, 'IP', '2011_Oct', 'cbddbbabaabacbababcbbddbccbcbdbdcdddbddccabadbbbadaccadcbdbcadccacbabcacbcdbbabccbbbddcbacabdbabcbbb', '2011A_IP_Question__2011_Oct', 103, 'e', 'IP_2011_Oct'));
        qlist.append(QuizModel(16, 'FE', '2012_Apr', 'dabcdbcacbaddacdccdbabaaabbbccbddbdddbacbdaccdabddabdacbbbdacbcbbdccbcccbbbccdca', '2012S_FE_AM_Question__2012_Apr', 80, 'c', 'FE_2012_Apr'));
        qlist.append(QuizModel(17, 'IP', '2012_Apr', 'dbaabcdaaddbbacdaccdbacbdcdccddcdabcaadbcaaabcbcdcdbcaaabbcdcababadabccbadaadcbccdcadcabccccaabccbca', '2012S_IP_Question__2012_Apr', 103, 'e', 'IP_2012_Apr'));
        qlist.append(QuizModel(18, 'FE', '2012_Oct', 'caccacbdbccdbccbbbaccbaacdaccacabccccbcbbdbddbbcbcbcbaacdbbcacddababdacacccdcdab', '2012Oct_FE_AM_Question__2012_Oct', 80, 'c', 'FE_2012_Oct'));
        qlist.append(QuizModel(19, 'IP', '2012_Oct', 'acdbddbdacacdadcaddadccddadbabbbccbbadcaaaabcaadcacaccbdccdddaaadcadabbcccddbabcbcaabbbadbdbcbddbcbc', '2012Oct_IP_Question__2012_Oct', 103, 'e', 'IP_2012_Oct'));
        qlist.append(QuizModel(20, 'FE', '2013_Apr', 'babccdbdccdddbbdcabcccdddbcdcacbcbabcccdcbbacdabddacccacbddccadacdcddcacaadbcbbc', '2013Apr_FE_AM_Question__2013_Apr', 80, 'c', 'FE_2013_Apr'));
        qlist.append(QuizModel(21, 'IP', '2013_Apr', 'cacacaacaaadbddcbbbdabcbcdacdbbcacbdcbddcaddbddbccdacbdbabbdcdbccdacbcaacddaccbcadbcacbbcccacbcaaada', '2013Apr_IP_Question__2013_Apr', 97, 'e', 'IP_2013_Apr'));
        qlist.append(QuizModel(22, 'FE', '2013_Oct', 'cbadddaccdacccaacabdbacbabccbdaabdcbbcbaaddcabacbdadabccdadbaddadcdabbabcbdcbdcb', '2013Oct_FE_AM_Question__2013_Oct', 80, 'c', 'FE_2013_Oct'));
        qlist.append(QuizModel(25, 'FE', '2014_Apr', 'dcabdacdadddbdbbddddbddcbdbbdcbdbadabdcdcdbadcaabdaccbbdcbdbbabaacdacdabacbbbabb', '2014S_FE_AM_Question__2014_Apr', 80, 'c', 'FE_2014_Apr'));
        qlist.append(QuizModel(26, 'FE', '2014_Oct', 'cbcadbabccccacdcccdbccbccbdbccccbdbaacaadbadcabccdabbaaddcabadbdcadbbbabdcbddbba', '2014Oct_FE_AM_Question__2014_Oct', 80, 'c', 'FE_2014_Oct'));
        qlist.append(QuizModel(29, 'FE', '2015_May', 'ddcacdcccdbbbaccaccadbaadddbccbbabbbbdbbddbabddcbcdacddbdbcdadbdbbdbaddbaddcddbc', '2015May_FE_AM_Question__2015_May', 80, 'c', 'FE_2015_May'));
        qlist.append(QuizModel(30, 'FE', '2015_Oct', 'bbdadbbcbcbacdcddadcabcbcdbbbddcdacbcbbdbaccbddbabbcdddabcadaaabcccdddcbcbdccccc', '2015A_FE_AM_Question__2015_Oct', 80, 'c', 'FE_2015_Oct'));
        qlist.append(QuizModel(34, 'FE', '2016_Oct', 'accbaacbcbcbcdabddaabcbadcdbdcbcbaccbcabbbcadccaabccdddcbabcbbcacbcdcbabbdacbbca', '2016A_FE_AM_Question__2016_Oct', 80, 'c', 'FE_2016_Oct'));
        qlist.append(QuizModel(36, 'IP', '2017_Apr', 'bcbddbbcbbcdddabacdbadbbdcabcabadaadbdcddbcadbcdddcaacaacdcdccccdbbcbccbdcaadccdcabdabcddccbbccbbdad', '2017S_IP_Question__2017_Apr', 100, 'c', 'IP_2017_Apr'));
        qlist.append(QuizModel(37, 'FE', '2017_Apr', 'bcaccbcdcbaabbaccadabaccdadccabbbbbadcdbcbbcddddcbccdcddddacbacbcaddcadaddcdbaac', '2017S_FE_AM_Question__2017_Apr', 80, 'c', 'FE_2017_Apr'));
        qlist.append(QuizModel(38, 'FE', '2017_Oct', 'abdcdcaacacbbcacdbcadcdbadbccbaabbbdababdcdaddabdbaadcabcbabbbccdbcbcddcdbcbbabb', '2017A_FE_AM_Question__2017_Oct', 80, 'c', 'FE_2017_Oct'));
        qlist.append(QuizModel(39, 'IP', '2017_Oct', 'cadccbdcdaddadcbabbcbabadcccddbabdabbddbaadabbdbbacbbdcbcdacbabadcbabaabccacbbcccbdcdbabadadaaaddbcd', '2017A_IP_Question__2017_Oct', 100, 'c', 'IP_2017_Oct'));
        qlist.append(QuizModel(40, 'FE', '2018_Mar', 'cdbcbdcbdccbcababbcaaacddcbacdbcbdaabccbbdadbcabdcbabddbcacbdbdcccadcdbbcbcdadbc', '2018S_FE_AM_Question__2018_Mar', 80, 'c', 'FE_2018_Mar'));
        qlist.append(QuizModel(41, 'IP', '2018_Mar', 'dbacbabacaabbbacbddcabbdbcbaacbbcdcddddabbaaddadbacdbadcadcbddaabbddababcdddcaabacbadcbdaccabdcaacbb', '2018S_IP_Question__2018_Mar', 100, 'c', 'IP_2018_Mar'));
        qlist.append(QuizModel(42, 'FE', '2018_Oct', 'bcdddcbabbccabcddbabddccacbdaabacbbbccaccdbcdbaaabbcacddaaaddccaccaacdcacbcaadbc', '2018A_FE_AM_Question__2018_Oct', 80, 'c', 'FE_2018_Oct'));
        qlist.append(QuizModel(43, 'IP', '2018_Oct', 'bcaacdbbcaccdaddbdccdcadbacccbbdcdaccccccdcccacdcacddcdaabddbacdbacacdbbcaacbacdadabdcbcbcccbcbbbcba', '2018A_IP_Question__2018_Oct', 100, 'c', 'IP_2018_Oct'));
        qlist.append(QuizModel(44, 'IP', '2019_Apr', 'acbcbbbcddbbaddadbbcbabbdccaadbbcbbbadaccddcdcbaaaaadbcabbbddacaaccccbbcdcbcbcdcbbdbbbcddbadabbbcdbd', '2019S_IP_Question__2019_Apr', 100, 'c', 'IP_2019_Apr'));
        qlist.append(QuizModel(45, 'FE', '2019_Apr', 'bcbbbbbaadbdbcadcdbabbcacbdcacbcadccdbbcbadabdbdbacccaacccaaaaabcbcdbcabdcabbabc', '2019S_FE_AM_Question__2019_Apr', 80, 'c', 'FE_2019_Apr'));
        qlist.append(QuizModel(47, 'IP', '2019_Oct', 'dabbbabbbcaaadbccaaabbccbcdacbbbccbdbcdbcdadddadddccdccbdabcbdadccadcaddabcdbaccaacbacccdbbabccbbdac', '2019A_IP_Question__2019_Oct', 100, 'c', 'IP_2019_Oct'));
        qlist.append(QuizModel(49, 'IP', '2020_Q2', 'ddacaabbbcadbccccddbacbddbbbcbabdabaaddccdacbabdddaaddcddbbcccaaddcdbbbbcdddacdddbdcdbddcdccaabcabad', '2020S_IP_Question__2020_Q2', 100, 'c', 'IP_2020_Q2'));
        qlist.append(QuizModel(50, 'FE', '2020_Oct', 'cadbdbddabaacdbbacbaccbacdddcdabccadbabbaccccbcdabdbdccdbcabccaaaaadaddbdcccdcdc', '2020A_FE_AM_Question__2020_Oct', 80, 'c', 'FE_2020_Oct'));
        qlist.append(QuizModel(51, 'IP', '2020_Oct', 'bcdcbdacbabbacbdabdccdadcdcbcbdcdbdaaadddababbccbcdcccaddddddcdabcadaacdcadabaadaacabbdacdcdcbdcbbaa', '2020A_IP_Question__2020_Oct', 100, 'c', 'IP_2020_Oct'));
        qlist.append(QuizModel(52, 'IP', '2021_Q4', 'aadacbabbcaabddbbbabacbdbcccabdddabadadcdbdccbdbaababddaacbbbdacdbbcddbdcabbdbcdaadddcbccccbbabbdcdd', '2021A_IP_Question__2021_Q4', 100, 'c', 'IP_2021_Q4'));
        qlist.append(QuizModel(53, 'FE', '2021_Q4', 'baddbabbcdcdbcccdadcccdbbddaddccbabcbccadcccdddcccccbcdaccababcdbcdcbccdcacdbadc', '2021A_FE_AM_Questions__2021_Q4', 80, 'c', 'FE_2021_Q4'));
        qlist.append(QuizModel(54, 'FE', '2021_Q2', 'bcbacbccaabccbadcdccaccdacddcdccbbbaaabbdccacdbcbcababbdbdddbabdccddcbcbaadcdbca', '2021S_FE_AM_Question__2021_Q2', 80, 'c', 'FE_2021_Q2'));
        qlist.append(QuizModel(55, 'IP', '2021_Q2', 'cacabdccddadcdaacccdcadddccacabcbccbdacdcbaccbccddcacabcdbbdbdbccbcacbcacbacccbadbacdccdcddabdcbaabb', '2021S_IP_Question__2021_Q2', 100, 'c', 'IP_2021_Q2'));
        qlist.append(QuizModel(56, 'IP', '2022_Apr', 'ccddbacaadcacdbcbddcccacbcbbdbbdbbbdacdadcdcbdbabdaabcbcddacdbaaaabcacdadcdbacdcdaabbddbbbcdbabbabbb', '2022S_IP_Question__2022_Apr', 100, 'c', 'IP_2022_Apr'));
        qlist.append(QuizModel(57, 'FE', '2022_Apr', 'aabccadacccbbdacadabddcddbcccbaccaabbbabbbcccdbacccdacdccadababcddaabcbbabacbdac', '2022S_FE_AM_Questions__2022_Apr', 80, 'c', 'FE_2022_Apr'));
        qlist.append(QuizModel(58, 'IP', '2022_Oct', 'ccdbbccddcbaccdccabcadbbdcdaabdcabbcdcddcabcbbcdaacdcaddabcbcdcdbbcabbccaacbcdbbcddcddabdbcdcbdabbab', '2022A_IP_Question__2022_Oct', 100, 'c', 'IP_2022_Oct'));
        qlist.append(QuizModel(59, 'FE', '2022_Oct', 'cbcdcccdaabdccacdbcccdacbbbabbabcbdaacccdacddcaaabcabbbadbadbdcaccadabbcaddbdbcc', '2022A_FE_AM_Question__2022_Oct', 80, 'c', 'FE_2022_Oct'));
        qlist.append(QuizModel(48, 'FE', '2020_Q2', 'bbbcccbabbcdbbddbdcccdbccbcbdbbbcbcabdcdbcaaddadcbdddccbaabdbbbccbacdbccbbcdbdbc', '2020S_FE_AM_Question__2020_Q2', 80, 'c', 'FE_2020_Q2'));
        qlist.append(QuizModel(46, 'FE', '2019_Oct', 'bcbbdccbacccdbdacbccbcbbcccbddabddbabcdabbdccdbabbbdcdccaacacddcabddddccddcdaddc', '2019A_FE_AM_Question__2019_Oct', 80, 'c', 'FE_2019_Oct'));
        for q in qlist:
            q.save()
