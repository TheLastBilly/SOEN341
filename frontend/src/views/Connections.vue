<template>
    <v-container grid-list-sm>
      <v-layout row wrap align-center justify-center fill-height>
        <v-flex xs12 sm12 lg12 md12>
          <v-card class="mx-12 mt-2">
            <v-card-text>
              <v-tabs v-model="tab"
                      fixed-tabs
                      background-color="blue"
                      dark
                      icons-and-text>
                <v-tab>
                  My Connections
                  <v-icon>mdi-account-multiple</v-icon>
                </v-tab>
                <v-tab>
                  Users You May Know
                  <v-icon>mdi-account-multiple-plus</v-icon>
                </v-tab>
              </v-tabs>

              <v-tabs-items v-model="tab">
                <v-tab-item>
                  <v-card>
                    <v-card-title>
                      Your Connections
                      <v-spacer></v-spacer>
                      <v-text-field
                        class="shrink"
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                        filled
                        rounded
                        dense/>
                    </v-card-title>
                    <v-data-table
                      :headers="headers2"
                      :items="connections"
                      :search="search"
                      hide-default-footer
                      hide-default-header>
                        <template v-slot:item="row">
                        <tr>
                          <td>{{row.item.username}}</td>
                          <td align="right">
                            <v-btn class="white--text text-capitalize mx-2"
                                small
                                rounded
                                color="blue"
                                @click="follow(row.item)">
                              Unfollow
                            </v-btn>
                            <v-btn class="white--text text-capitalize"
                                   small
                                   rounded
                                   outlined
                                   color="blue"
                                   @click="seeProfile(row.item)">
                              See Profile
                            </v-btn>
                          </td>
                        </tr>
                      </template>
                      </v-data-table>
                  </v-card>
                </v-tab-item>
                <v-tab-item>
                  <v-card>
                    <v-card-title>
                      Find Users
                      <v-spacer></v-spacer>
                      <v-text-field
                        class="shrink"
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                        filled
                        rounded
                        dense/>
                    </v-card-title>
                    <v-data-table
                      :headers="headers1"
                      :items="users"
                      :search="search"
                      hide-default-footer
                      hide-default-header>
                      <template v-slot:item="row">
                        <tr>
                          <td>{{row.item.username}}</td>
                          <td align="right">
                            <v-btn class="white--text text-capitalize mx-2"
                                small
                                rounded
                                color="blue"
                                @click="follow(row.item)">
                              Follow
                            </v-btn>
                            <v-btn class="white--text text-capitalize"
                                   small
                                   rounded
                                   outlined
                                   color="blue"
                                   @click="seeProfile(row.item)">
                              See Profile
                            </v-btn>
                          </td>
                        </tr>
                      </template>
                    </v-data-table>
                  </v-card>
                </v-tab-item>
              </v-tabs-items>
            </v-card-text>
          </v-card>

        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Connections',
  data: () => ({
      currentUser: '',
      tab: null,
      search: '',
      users: [],
      connections: [],
      headers1: [
          { text: 'Username', align: 'start', value: 'username'},
          { text: 'Actions', align: 'right', value: 'actions' }
      ],
      headers2: [
          { text: 'Username', align: 'start', value: 'username'},
          { text: 'Actions', align: 'right', value: 'actions' }
      ],
      loading: false,
      snackbarError: false,
      errorMessage: 'Unable to post!',
      snackbarApproved: false,
      approvedMessage: 'New post successfully created!',
      timeout: 5000,
      showPostDialog: false,
      allUsers: null
  }),
  methods: {
    getAllUsers() {
      this.loading = true;
      axios.get('http://localhost:8000/api-auth/user/getAll').then(response => {
        this.users = response.data
        this.users = this.users.filter(item => item.username !== this.currentUser)
        var token = this.$session.get('token')
        axios.get('http://localhost:8000/api-auth/user/following/', {headers: {Authorization: 'JWT ' + token}}).then(response => {
          for(var i in response.data){
            this.users = this.users.filter(item => item.username !== response.data[i].username)
          }
        }).catch(e => {
          console.log(e)
        })
        this.snackbarApproved = true
      }).catch(e => {
        this.snackbarError = true
        this.loading = false
        console.log(e)
      })
    },
    follow(user) {
      var token = this.$session.get('token')
      axios.get('http://localhost:8000/api-auth/user/follow/' + user.username, {headers: {Authorization: 'JWT ' + token}}).then(response => {
        console.log(response.data)
        this.myConnections()
        this.getAllUsers()
      }).catch(e => {
        console.log(e)
      })
    },
    myConnections() {
      var token = this.$session.get('token')
      axios.get('http://localhost:8000/api-auth/user/following/', {headers: {Authorization: 'JWT ' + token}}).then(response => {
        this.connections = response.data
        //console.log(response.data)
      }).catch(e => {
        console.log(e)
      })
    },
    newPost() {
      this.showPostDialog = true
    },
    seeProfile(user) {
      console.log(user)
      this.$router.push({
            path: '/userprofile',
            query: { userprofile: user }})
    },
    loadUser(){
      this.currentUser = this.$session.get('current_user')
    }
  },
  computed: {
  },
  mounted() {
    this.loadUser()
    this.getAllUsers()
    this.myConnections()
  }
}
</script>
