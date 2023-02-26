package main

import (
	"database/sql"
	"fmt"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
	_ "github.com/godror/godror"
)

func oracletest(sleep_time []int) {
	var db *sql.DB
	db, err := sql.Open("godror", `user="findpt" password="findpt" connectString="172.16.6.131:1521/utf8?expire_time=30"`)
	defer db.Close()
	err = db.Ping()
	if err != nil {
		fmt.Printf("Open err: %v\n", err)
		return
	}
	fmt.Printf("********oracle test start: %v******** \n", time.Now().String())
	for _, t := range sleep_time {
		fmt.Printf("****oracle sleep %ds, now is %v \n", t, time.Now().String())
		rows, _ := db.Query(fmt.Sprintf("select findpt.TEST_SLEEP(%d),current_date from dual", t))
		rows.Close()
	}
	fmt.Printf("********oracle test finish: %v******** \n", time.Now().String())
}

func mysqltest(sleep_time []int) {
	var dbm *sql.DB
	dbm, err := sql.Open("mysql", "abcuser1:abcuser1@tcp(120.92.102.61:3306)/mysql")
	defer dbm.Close()
	err = dbm.Ping()
	if err != nil {
		fmt.Printf("Open err: %v\n", err)
		return
	}
	fmt.Printf("********mysql test start: %v******** \n", time.Now().String())
	for _, t := range sleep_time {
		fmt.Printf("****mysql sleep %ds, now is %v \n", t, time.Now().String())
		rows, _ := dbm.Query(fmt.Sprintf("select sleep(%d)", t))
		rows.Close()
	}
	fmt.Printf("********mysql test finish: %v******** \n", time.Now().String())
}

func main() {
	// sleep_time := []int{5, 7, 9, 1, 1}
	sleep_time := []int{57, 63, 60*5 + 3, 60*30 - 3, 60*30 + 3, 60*60 - 3, 60*60 + 3}
	fmt.Printf("********main start: %v******** \n", time.Now().String())
	time.Sleep(10 * time.Second)
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		defer wg.Done()
		mysqltest(sleep_time)
	}()
	go func() {
		defer wg.Done()
		oracletest(sleep_time)
	}()
	wg.Wait()
	fmt.Printf("********main finish: %v******** \n", time.Now().String())
}
