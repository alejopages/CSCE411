#include <stdio.h>
#include <stdlib.h>
#include <sys/times.h>

#include "record.h"


int main(int argc, char **argv)
{
    int i,j, currMax = 0, currUser;
	char *loc;

    char filename[1024];
    FILE *fp = NULL;
    
    struct timeval time_start, time_end;
    
    /* start time */
    gettimeofday(&time_start, NULL);
    
    for (i = 0; i <= 1999; i++) {
        /* open the corresponding file */  
        sprintf(filename, "record_%06d.dat", i);
    
        fp = fopen(filename,"rb");
    
        if (!fp) {
            fprintf(stderr, "Cannot open %s\n", filename);
            continue;
        }
        
        /* read the record from the file */
        record_t *rp = read_record(fp);
    
        /* =========== start of data processing code ================ */
    
        loc = strtok(rp->location, ",");
		loc = strtok(NULL, ",");
		if(loc == NULL) {
			continue;
		}
		if(strcmp("Nebraska", loc) == 0) {
			int msgCount = 0;
			for(j = 0; j < rp->message_num; j++){
				message_t *msg = &(rp->messages[j]);
				if(msg->hour >= 8 && (msg->hour < 9 || (msg->hour == 9 && msg->minute == 0))) {
					msgCount = msgCount + 1;
				}
			}
			if(msgCount > currMax) {
				currUser = rp->id;
			}
		}
        
        /* =========== end of data processing code ================ */    
    
        /* free memory */
        free_record(rp);
    
        /* close the file */
        fclose(fp);
    }    
        
    
    /* end time */
    gettimeofday(&time_end, NULL);
    
    float totaltime = (time_end.tv_sec - time_start.tv_sec)
                    + (time_end.tv_usec - time_start.tv_usec) / 1000000.0f;
                    
         
    printf("\n\nThe user from Nebraska with most messages between 8am-9am: %d user id", currUser);     
    printf("\n\nProcess time %f seconds\n", totaltime);
    
    return 0;
}
