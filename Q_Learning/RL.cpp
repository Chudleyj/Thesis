#include "RL.h"

int main(int argc, char **argv)
{
  std::cout << "Called" << std::endl;
  
  portfolioData portfolio; //Start with 'X' (See RL.h) dollars
  RLdata RL(atof(argv[1]), atof(argv[2]));
  
  std::vector<bool> actions; //write actions to here for file output.
  std::vector<double> QS; //write Qsell to here for file output.
  std::vector<double> QB; //write Qbuy to here for file output.
  std::vector<double>profVec;
 
    
  //Fill in prices from CSV file
  const std::vector<double> historicalPrices = get_CSV_data();
  double ProbabilityOfBuy = 0.0;
 
  for(int t = 0; t < historicalPrices.size()-1; t++)
  {//Pass t
    //Start the RL by choosing an action
    ProbabilityOfBuy = softMax(RL);
      
      // Choose action, and update assets a year later.
    chooseAction(RL,ProbabilityOfBuy,portfolio,historicalPrices,t);
      
    //Action was taken, reward has been given, now update Q
    updateQvalues(RL, portfolio);
      
    //Write values to vectors for file output
    actions.push_back(RL.action); //Write action to vec for output at end
    QS.push_back(RL.Qsell);
    QB.push_back(RL.Qbuy);
    profVec.push_back(portfolio.currentAssets - 10273.1);
    ProbabilityOfBuy = 0.0;
   }
  //RL is over, sell any left overs to calc total profits.
  std::cout << "Profit: " << portfolio.currentAssets - 10273.1;
 // ToFile((portfolio.currentAssets - 10273.1), QS, QB, actions, RL.alpha, RL.beta);
  ToFile2(profVec, argv[3]);
  ToFile3(portfolio.currentAssets-10273.1, RL.alpha, RL.beta, argv[3]);
}

std::vector<double> get_CSV_data()
{
    std::ifstream ip(_FILE_PATH);
   
    if(!ip.is_open())
        std::cout << "Error opening file." << std::endl;
    
    std::vector<double> vec;
    std::string temp;
    while(std::getline(ip, temp))
        vec.push_back(atof(temp.c_str()));
    
    ip.close();
    return vec;
}

double softMax(const RLdata &RL)
{
    //1/(1+e^(Q(action)-Q(otherAction)*Beta)
    return(1/(1+exp((RL.Qsell-RL.Qbuy)*RL.beta)));
}

void chooseAction(RLdata &RL, const double &Pbuy, portfolioData &env, const std::vector<double> price, const int count)
{
    auto p = random_double();
    RL.action = p < Pbuy;
    //std::cout <<"rand: " << p << " prob: " << Pbuy << " action: " <<  RL.action << " QB: " << RL.Qbuy << " QS: " << RL.Qsell << std::endl;
    
    if(RL.action || env.currentStocksOwned < 0)
        buy(env, RL, price, count);
    else
        sell(env, RL, price, count);
}

double random_double()
{
    std::random_device rd;
    std::mt19937 e2(rd());
    std::uniform_real_distribution<> dist(0, 1);
    return dist(e2);
}

void buy(portfolioData &env, RLdata &RL, const std::vector<double> &price, const int &count)
{
    env.previousAssets = env.currentAssets;
    env.currentStocksOwned++;
    env.currentBank = env.currentBank - price[count];
    env.currentAssets = env.currentBank + (env.currentStocksOwned * price[count+1]);
    //std::cout <<" Buy prev " <<  env.previousAssets << " curr " <<  env.currentAssets << " stock " << env.currentStocksOwned << " bank "<< env.currentBank
    //<< " price " <<price[count] << " price +1 " << price[count+1] << std::endl;
}

void sell(portfolioData &env, RLdata &RL, const std::vector<double> price, const int count)
{
    env.previousAssets = env.currentAssets;
    env.currentStocksOwned--;
    env.currentBank = env.currentBank + price[count];
    env.currentAssets = env.currentBank + (env.currentStocksOwned * price[count+1]);
   // std::cout <<"Sell prev " <<  env.previousAssets << " curr " <<  env.currentAssets << " stock " << env.currentStocksOwned << " bank "<< env.currentBank
   // << " price " <<price[count] << " price +1 " << price[count+1] << std::endl;
}

void updateQvalues(RLdata &RL, const portfolioData &env)
{
    double r = env.currentAssets - env.previousAssets;
   // std::cout<<"r: " << r << std::endl;
    if(RL.action)
        RL.Qbuy = (1 - RL.alpha) * RL.Qbuy + (RL.alpha*r);
    else
        RL.Qsell = (1 - RL.alpha) * RL.Qsell + (RL.alpha*r);
}

void ToFile(const double &profits, const std::vector<double> &Qsells,
            const std::vector<double> & Qbuys,const std::vector<bool> & actions,
            const double &alpha, const double &beta)
{
    std::ofstream file;
    
    file.open ("RL_Profits.txt", std::ios_base::app);
        file << std::fixed << profits << std::endl;
    file.close();
    
    file.open ("RL_Qsells.txt", std::ios_base::app);
    for(int i = 0; i < Qsells.size(); i++)
        file << std::fixed << Qsells[i] << std::endl;
    file.close();
    
    file.open ("RL_Qbuys.txt", std::ios_base::app);
    for(int i = 0; i < Qbuys.size(); i++)
        file << std::fixed << Qbuys[i] << std::endl;
    file.close();
    
    file.open ("RL_Actions.txt", std::ios_base::app);
    for(int i = 0; i < actions.size(); i++)
        file << actions[i] << std::endl;
    file.close();
    
    file.open ("RL_AlphaBeta.txt", std::ios_base::app);
    file << alpha << " " << beta << " " << std::endl;
    file.close();
}

void ToFile2(const std::vector<double> & profits, std::string fileNum)
{
    std::ofstream file;
    std::string fileName = "RLprofits";
    fileName += fileNum;
    fileName += ".txt";
    file.open ("./data/0.21_6.7_data.txt", std::ios_base::app);
    for(int i = 0; i < profits.size(); i++)
        file << std::fixed << profits[i] << std::endl;
    file << "NEW SET" << std::endl;
    file.close();
}

void ToFile3(const double &profits, const double &alpha, const double &beta, const std::string &fileNum)
{
    std::ofstream file;
    file.open("./data/data2.txt", std::ios_base::app);
    file << std::fixed << alpha << " " << beta << " " << profits << std::endl;
    file.close();
}
