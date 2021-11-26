function answer = Prewitt_H(p)
    horizontal = [-1,-1,-1;0,0,0;1,1,1];
    q = p.*horizontal;
    count = sum(sum(q));
answer =count;
