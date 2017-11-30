#include <iostream>
#include <cpr/cpr.h>

int main(int argc, char** argv) {
    const auto r = cpr::Get(cpr::Url{"http://icanhazip.com/"});
    if (r.status_code != 200) {
        std::cout << "Return code is " << r.status_code << std::endl;
        std::abort();
    }
    std::cout << r.text;
}
