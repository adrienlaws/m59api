#ifndef APIFN_H
#define APIFN_H

#include <winsock2.h>  // For SOCKET and related types
#include <windows.h>   // For MAX_PATH, HINSTANCE, etc.

// Forward declarations to avoid unnecessary includes
typedef struct connection_node connection_node;
typedef struct buffer_node buffer_node;
typedef struct admin_data admin_data;
typedef struct game_data game_data;
typedef struct trysync_data trysync_data;
typedef struct synched_data synched_data;
typedef struct resync_data resync_data;




#define SESSION_STATE_BYTES 120  // Define if not already defined
#define SEED_COUNT 5
unsigned int seeds[SEED_COUNT];  // Ensure SEED_COUNT is defined


typedef int Bool;  // Define Bool properly
#define True 1
#define False 0

enum { STATE_ADMIN, STATE_GAME, STATE_TRYSYNC,
    STATE_SYNCHED, STATE_RESYNC, STATE_MAINTENANCE };

typedef struct account_node
{
   int account_id;
   char *name;
   char *password;
   int type;
   int credits;			/* remember, stored as 1/100 of a credit */
   INT64 last_login_time;
   INT64 suspend_time;
   struct account_node *next;
} account_node;

typedef struct {
    char name[32];
    int account_id;
    int version;
    int session_id;
    char connection[32];
    char state[32];
    int object_id;
} ApiWhoEntry;

typedef struct {
    char names[256][32];  // Store up to 256 players, max 32-char names
    int count;
} player_list_t;

typedef struct
{
   int session_id;
   connection_node *conn;
   Bool active;
   Bool connected;
   INT64 connected_time;
   int state;
   Bool hangup;
   INT64 timer;
   char session_state_data[SESSION_STATE_BYTES];

   /* these guys are just set to point to session_state_data */
   union
   {
      admin_data *adm;
      admin_data *mtn; /* same data as admin_data */
      game_data *game;
      trysync_data *ts;
      synched_data *syn;
      resync_data *resyn;
   };

   account_node *account;
   Bool login_verified;
   Bool blak_client;

   /* data about the user's machine, only valid if blak_client is true */
   char version_major;
   char version_minor;
   int os_type;
   int os_version_major;
   int os_version_minor;
   int machine_ram;
   int machine_cpu;
   short screen_x;
   short screen_y;
   short screen_color_depth;
   short partner;
   int displays_possible;
   int bandwidth;
   int reserved;

   Bool exiting_state;		
   int last_download_time; 

   unsigned int seeds[SEED_COUNT]; 
   Bool seeds_hacked;
   unsigned int secure_token;
   const char* sliding_token;

   HANDLE muxReceive;  // Mutex type from Windows API
   buffer_node *receive_list;
   int receive_index; 

   HANDLE muxSend;  // Mutex type from Windows API
   buffer_node *send_list;

} session_node;

// API functions
void InitAPIServer();
player_list_t GetOnlinePlayers();
int ApiWho(ApiWhoEntry *out_list, int max_entries);
void ForEachSession(void (*func)(session_node*));

#endif // APIFN_H
