#include <iostream>
#include <fstream>
#include <vector>
#include <stdlib.h>
#include <random>
#include <set>
#include <iterator>
#include <functional>
#include <algorithm>
#include <initializer_list>
#include <math.h> //Euler's number
#include <cmath>
#include <cstdlib>
#include <random>
#include <stdlib.h>     /* atoi */

const int _DATA_SIZE = 27809;
const std::string _FILE_PATH = "DJI2.csv";

struct portfolioData
{
    double previousAssets = 10000;
    double currentAssets = 10000;
    double currentBank = 10000;
    double profits;
    int currentStocksOwned = 0;
};

struct RLdata
{
  const double alpha;
  const double beta;
  bool action; //0  = BUY, 1 = SELL
  double Qbuy = 0;
  double Qsell = 0;
  RLdata(const double &a, const double &b) : alpha(a), beta(b){}
};

std::vector<double> get_CSV_data();
double softMax(const RLdata &);
void chooseAction(RLdata &, const double &, portfolioData &, const std::vector<double>, const int);
double random_double();
void buy(portfolioData &, RLdata &, const std::vector<double>, const int);
void sell(portfolioData &, RLdata &, const std::vector<double>, const int);
void updateQvalues(RLdata &, const portfolioData &);




void ToFile(const std::vector<double>&, const std::vector<double> &, const                  std::vector<double> &,
            const std::vector<bool> &, const std::vector<double> &,
            const double &, const double &);
