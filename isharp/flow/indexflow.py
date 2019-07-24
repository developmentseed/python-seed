import luigi


class MarketDataInput(luigi.ExternalTask):
    waitingOn=luigi.Parameter()
    def output(self):
        return [luigi.LocalTarget("c:\\temp\\{}.txt".format(self.waitingOn))]


class TrivialInput(luigi.Task):
    trivparam=luigi.Parameter(default="trivial")
    def run(self):
        print("_____________running TRIV TRIV__________________."+ self.trivparam)
        with open("c:\\temp\\{}.txt".format(self.trivparam),'w') as output_file:
            output_file.write("blah")

    def output(self):
        return [luigi.LocalTarget("c:\\temp\\{}.txt".format(self.trivparam))]


class IndexCalculation(luigi.Task):
    index_name=luigi.Parameter()
    def run(self):
        print("_____________running__________________")

    def requires(self):
        reqs = [MarketDataInput(waitingOn=n) for  n in ["luigi","luigo","luigz"] ]
        reqs.append(TrivialInput(trivparam=self.index_name+"_triv"))
        return reqs

if __name__ == '__main__':
    luigi.build([IndexCalculation(index_name='triv_trov_zzz')])
      # luigi.build([MarketDataInput(waitingOn='luigi_')])




