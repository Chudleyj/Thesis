#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <string>


int main()
{
   /* for(double a = 0.01; a < 1; a += 0.01){
        for(double b = 0.1; b < 10; b += 0.1){
            for(int i = 0; i < 100; i++){
                std::string tempa = std::to_string(a);
                std::string tempb = std::to_string(b);
                std::string filenum = std::to_string(a) + " " + std::to_string(b) + ".txt";
                const char* const args[] = {"./RL", tempa.c_str(), tempb.c_str(),filenum.c_str(), nullptr};
                std::cout << std::endl << "Calling: " << a << " " << b << std::endl;
                if (fork() == 0)
                    execvp(args[0], const_cast<char*const*>(args));
                else
                    wait(NULL);
                }
            }
        }*/
    std::string a = "0.21";
    std::string b = "6.7";
    for (int i = 1; i <= 30; i++){
        int count = i;
        std::string temp = std::to_string(count);
        const char* const args[] = {"./RL", a.c_str(), b.c_str(), temp.c_str(), nullptr};
        std::cout << std::endl << "Calling: " << a << " " << b << std::endl;
        if (fork() == 0)
            execvp(args[0], const_cast<char*const*>(args));
        else
            wait(NULL);
    }
    return 0;
    /*
    std::string a = "1";
    for(double b = 0.1; b < 10; b+= 0.1){
        for(int i = 0; i < 100; i++){
            std::string tempb = std::to_string(b);
            std::string tempc = "test";
            const char* const args[] = {"./RL", a.c_str(), tempb.c_str(),tempc.c_str(), nullptr};
            std::cout << std::endl << "Calling: " << a << " " << b << std::endl;
            if (fork()==0)
                execvp(args[0], const_cast<char*const*>(args));
            else
                wait(NULL);
        }
    }*/
}


