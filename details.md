## Day 15

Initially solved by looking at each row and computing the locations where the deacon cannot be, using an ADT of unions of segments.  This is very slow where performed 4,000,000 times.

Instead, we use the structure of the problem to simplify things.  There is a unique point not covered by one of the unit balls (in the 1-norm).  Such a gap can only occur where a number of the balls stop overlapping:

    *****###
    ****####
    *** ####
    **.--###
    *...--##

Two balls not matching up exactly would also leave a gap, but you would get more than one gap.

We search for when $(x,y)$ can be a gap between balls centred at $(s_x^i, s_y^i)$ of size $d_i$, for $i=1,2$.  This occurs when $(x-1,y)$ is in the boundary of ball 1, and $(x+1,y)$ is in the boundary of ball 2 (wlog, as we'll test all ordered pairs).  So
$$ |s_x^1 - (x-1)| + |s_y^1-y| = d^1, \quad |s_x^2 - (x+1)| + |s_y^2-y| = d^2, $$
and also $s_x^1 \leq x-1, s_x^2 \geq x+1$.  So we seek $s_x^1+1 \leq x \leq s_x^2-1$ with $x-1-s_x^1 + |s_y^1-y| = d^1$ and $s_x^2-x-1+|s_y^2-y|=d^2$.  That is,
$$ x = d^1 - |s_y^1-y| + 1 + s_x^1 = s_x^2-1+|s_y^2-y|-d^2. $$
For this $x$, automatically $s_x^1+1 \leq x \leq s_x^2-1$, assuming that $y$ is valid, namely $|s_y^1-y| \leq d^1$ and $|s_y^2-y| \leq d^2$.

We then test the case $y\leq s_y^1$ and $y\leq s_y^2$.  For this case, we need
$$ s_y^1-d^1 \leq y\leq s_y^1, \quad s_y^2-d^2 \leq y \leq s_y^2,
\quad 
d^1 - s_y^1+y + 1 + s_x^1 = s_x^2-1+s_y^2-y-d^2,
$$
so $2y = s_x^2 - s_x^1 - 2 + s_y^2 + s_y^1 - d^2 - d^1$.

Alternatively, $y\geq s_y^1$ and $y\geq s_y^2$.  For this case, we need
$$ s_y^1 \leq y \leq s_y^1+d^1, \quad s_y^2 \leq y \leq s_y^2+d^2
\quad 
d^1 - y + s_y^1 + 1 + s_x^1 = s_x^2 - 1 + y - s_y^2 - d^2
$$
so $2y = d^1 +d^2 + s_y^1 +s_y^2 + 2 + s_x^1 - s_x^2$.

The other two cases don't make sense, as these correspond to two balls never overlapping (just being of gap size 1 distant).


## Day 16

Spent some time on this one.  I wondered if there was a dynamic programming approach, but I couldn't see what an "optimal substructure" would be.  Searching all possible routes is impossibly slow, but a simple backtracking algorithm works, in the end.

The 2nd part is very slow even with the backtracking idea.
