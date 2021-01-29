import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';


import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Course } from './course';

@Injectable({
  providedIn: 'root'
})
export class BackendConnectionService {

  private API_URL = 'http://127.0.0.1:5000/';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor( private http: HttpClient ) { }

  /** GET all courses from the server */
  getCourses(): Observable<Course[]> {
    const url =`${this.API_URL}allCoursesDetails`;
    return this.http.get<Course[]>(url)
      .pipe(
        tap(_ => ""),
        catchError(this.handleError<Course[]>('getCourses', []))
      );
  }

  /** GET hero by id. Will 404 if id not found */
  getCourse(id : String): Observable<Course> {
    const url = `${this.API_URL}CourseById`;
    return this.http.post<Course>(url, JSON.stringify({'idCourse':id})).pipe(
      tap(_ => ''),
      catchError(this.handleError<Course>(`getCourse id=${id}`))
    );
  }

  getSimilarCourses(id : String): Observable<Course[]> {
    const url = `${this.API_URL}similarCourses`;
    return this.http.post<Course[]>(url, JSON.stringify({'idCourse':id})).pipe(
      tap(_ => ''),
      catchError(this.handleError<Course[]>(`getSimilarCourses id=${id}`))
    );
  }

  getRecommandUsers(id : String): Observable<Course[]> {
    const url = `${this.API_URL}recommendUsers`;
    return this.http.post<Course[]>(url, JSON.stringify({'idCourse':id})).pipe(
      tap(_ => ''),
      catchError(this.handleError<Course[]>(`getRecommandUsers id=${id}`))
    );
  }

  getSimilarReview(id : String): Observable<Course[]> {
    const url = `${this.API_URL}similarReview`;
    return this.http.post<Course[]>(url, JSON.stringify({'idCourse':id})).pipe(
      tap(_ => ''),
      catchError(this.handleError<Course[]>(`getSimilarReview id=${id}`))
    );
  }

  getCoursesWithFilters(filters): Observable<Course[]> {
    const url =`${this.API_URL}coursesWithFilters`;
    console.log(JSON.stringify({'filters':filters}))
    return this.http.post<Course[]>(url,JSON.stringify({'filters':filters})).pipe(
        tap(_ => ""),
        catchError(this.handleError<Course[]>('getCoursesWithFilters', []))
      );
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
  
      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead
  
      // TODO: better job of transforming error for user consumption
     // this.log(`${operation} failed: ${error.message}`);
  
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
