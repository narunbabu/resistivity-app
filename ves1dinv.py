# % Function Jacobian %
def jacobian(ab2,x,r,t,lr,lt,roa,roa1):
    par = 0.1;
    r2 = r;
    for i2 in range( lr):
        r2[i2] = (r[i2]*par)+r[i2];
        for ii in range(len(x)):
            s = ab2[ii];
            [g] = VES1dmod (r2,t,s);
            roa2(ii,:) = g;

        A1[:,i2] = [(roa2-roa1)/(r[i2]*par)]*r[i2]./roa;
        r2 = r;

    t2 = t;
    for i3 in range(lt):
        t2[i3] = (t[i3]*par)+t[i3];
            for ii in range(len(x)):
                s = ab2[ii];
                [g] = VES1dmod (r,t2,s);
                roa3[ii,:] = g;

        A2[:,i3] = [(roa3-roa1)/(t[i3]*par)]*t[i3]./roa;
        t2 = t;

    A = [A1, A2];
    return A