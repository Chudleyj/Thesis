#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <string>
int main()
{
    for(double a = 0.1; a < 1; a += 0.1){
        for(double b = 0.1; b < 1; b += 0.1){
            for(double c = 0.1; c < 1; c+= 0.1){
                std::string tempa = std::to_string(a);
                std::string tempb = std::to_string(b);
                std::string tempc = std::to_string(c);
                const char* const args[] = {"./RL", tempa.c_str(), tempb.c_str(), tempc.c_str(), nullptr};
                std::cout << "Calling: " << a << " " << b << " " << c << std::endl;
                if (fork() == 0)
                    execvp(args[0], const_cast<char*const*>(args));
                else
                    wait(NULL);
            }
        }
    }
    return 0;
}


