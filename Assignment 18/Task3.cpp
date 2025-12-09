#include <iostream>

int factorial(int n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}

int main() {
    int number;
    std::cout << "Enter a number: ";
    std::cin >> number;
    std::cout << factorial(number) << '\n';
    return 0;
}