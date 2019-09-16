#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

#define DBG

#define __FUNC_ENTER__ printf("ENTER:%s\n", __func__);
#define __FUNC_LEAVE__ printf("LEAVE:%s\n", __func__);


static int g_sockfd = 0;
static char *ADDR = "127.0.0.1";
static int PORT = 10000;
static int g_wait_done = 0;

typedef enum {
	FSM_STATE_NORMAL = 0,
	FSM_STATE_WAIT,
	FSM_STATE_READY,
	FSM_STATE_MAX,
} fsm_state_e;

int fsm_progress(fsm_state_e current, void *data)
{
	int ret = 0;
	printf("fsm_progress:%d\n", current);
	switch (current) {
		/* recv msg from srv */
		case FSM_STATE_NORMAL: {
			char buffer[1024] = {};
			if ((ret = recv(g_sockfd, buffer, sizeof(buffer), 0)) < 0) {
				printf("fail to recv\n");
				return -1;
			} else {
				printf("recv:%s\n", buffer);
			}
			break;
		}

		/* send signal graceful-restart with timeout */
		case FSM_STATE_WAIT: {
			g_wait_done = 0;
			int cnt = 0;
			do {
				sleep(1);
				cnt++;
			} while (g_wait_done == 0 && cnt < 10);
			printf ("state_wait\n");
			break;
		}

		case FSM_STATE_READY: {
			char *buf = "$MTD,CONFIRM,10.0.0.1,0<";
			while (1) {
				sleep(1);
				if (send(g_sockfd, buf, strlen(buf), 0) < 0) {
					printf("fail to send data\n");
				} else {
					printf("sent\n");
					break;
				}
			}
			printf("DONE: send msg\n");
			break;
		}
		default:
			return -1;
			break;
	}

	return 0;
}

fsm_state_e get_next_state(fsm_state_e curr)
{
	fsm_state_e next_to = curr + 1;
	if (next_to == FSM_STATE_MAX) {
		next_to = FSM_STATE_NORMAL;
	}

	return next_to;
}

static int mtd_connect(char *serv_ip, int port)
{
	__FUNC_ENTER__
	int sockfd = 0;
	struct sockaddr_in serv_addr;
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == -1) {
		printf("fail to create socket\n");
		return -1;
	}
	bzero(&serv_addr, sizeof(serv_addr));

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = inet_addr(serv_ip);
	serv_addr.sin_port = htons(port);

	if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) != 0) {
		printf ("fail to connect\n");
		return -1;
	}

	g_sockfd = sockfd;
	send(g_sockfd, "hello", strlen("hello"), 0);
	return 0;
}

static int mtd_disconnect()
{
	__FUNC_ENTER__
	if (g_sockfd)
		close(g_sockfd);
	DBG("aaa%s\n", "aa");
}

void *myThreadFun(void *vargp)
{
	__FUNC_ENTER__
	static fsm_state_e current = FSM_STATE_NORMAL;
	int ret = 0;
	mtd_connect("127.0.0.1", 10000);
	while(1) {
		ret = fsm_progress(current, NULL);
		if (ret != 0) {
			printf("fail to progress\n");
			break;
		}
		current = get_next_state(current);
	}
	mtd_disconnect();
	return NULL;
}

int main() {
	pthread_t thread_id;
	printf("Before thread\n");
	pthread_create(&thread_id, NULL, myThreadFun, NULL);
	printf("Joining Thread\n");
	pthread_join(thread_id, NULL);
	printf("After Thread\n");

	exit(0);
}
