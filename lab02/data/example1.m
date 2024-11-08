# special functions, initializations

A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere

# initialize 3x3 matrix with specific values
E1 = [ [1, 2, 3],
       [4, 5, 6],
       [7, 8, 9] ] ;

A[1,3] = 0 ;

x = 2;
y = 2.5;

for i = 1:N-6+8 {
    if(i<=N/16)
        print i;
    else if(i<=N/8)
        break;
    else if(i<=N/4)
        continue;
    else if(i<=N/2)
        return 0;
}