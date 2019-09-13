#!/usr/bin/env python



class InLiftTest():

    def testCoords(self,p3):
        p1 = [0,0]
        p2 = [5,-3]
        # p3 = [-1.5,0.3]

        xmin = min(p1[0],p2[0])
        ymin = min(p1[1],p2[1])
        xmax = max(p1[0],p2[0])
        ymax = max(p1[1],p2[1])


        if xmin <= p3[0] <= xmax and ymin <= p3[1] <= ymax:
            return True
        else:
            return False





if __name__ == '__main__':
    test = InLiftTest()
    if test.testCoords([2,-1]):
        print "Inside"
    else:
        print "Outside"
    # navTest.setup2()


    #while loop keeps script alive for the threads to run. Super bad but
    #can change for the real thing.
    #x = 1
    #while (True):
    #    y= x + 1
