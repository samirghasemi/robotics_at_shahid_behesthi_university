function answer = Prewitt_V(p)
    vertical = [-1,0,1;-1,0,1;-1,0,1];
    q = p.*vertical;
    count = sum(sum(q));
answer =count;
