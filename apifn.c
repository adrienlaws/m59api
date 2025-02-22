#include <Python.h>
#include <string.h>      // For strncpy
#include <stdlib.h>      // For system
#include "apifn.h"



static player_list_t api_player_list;

void CollectOnlinePlayers(session_node *s)
{
    if (s->state == STATE_GAME && s->account)
    {
        if (api_player_list.count < 256)
        {
            strncpy(api_player_list.names[api_player_list.count], s->account->name, 31);
            api_player_list.names[api_player_list.count][31] = '\0';  // Null-terminate
            api_player_list.count++;
        }
    }
}
int num_sessions;
session_node *sessions;

void ForEachSession(void (*callback_func)(session_node *s))
{
	int i;

	/* the callback function shouldn't delete the session,
	in case it becomes a linked list */

	for (i=0;i<num_sessions;i++)
		if (sessions[i].connected)
			callback_func(&sessions[i]);
}

player_list_t GetOnlinePlayers()
{
    api_player_list.count = 0;  // Reset player list count
    ForEachSession(CollectOnlinePlayers);  // Iterate over all active sessions
    return api_player_list;
}

void InitAPIServer()
{
    system("uvicorn fastapi.main:app --host 127.0.0.1 --port 8000 &");
}

static PyObject* py_get_online_players(PyObject* self, PyObject* args)
{
    player_list_t players = GetOnlinePlayers();
    PyObject* player_list = PyList_New(players.count);
    for (int i = 0; i < players.count; i++)
    {
        PyObject* player_name = PyUnicode_FromString(players.names[i]);
        PyList_SetItem(player_list, i, player_name);
    }
    return player_list;
}

static PyMethodDef ApiMethods[] = {
    {"get_online_players", py_get_online_players, METH_VARARGS, "Get online players"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef apimodule = {
    PyModuleDef_HEAD_INIT,
    "apifn",
    NULL,
    -1,
    ApiMethods
};

PyMODINIT_FUNC PyInit_apifn(void)
{
    return PyModule_Create(&apimodule);
}