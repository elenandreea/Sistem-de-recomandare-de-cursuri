import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { CoursesListComponent } from './courses-list/courses-list.component';
import { SingleCourseComponent } from './single-course/single-course.component';
import { CourseListElemComponent } from './course-list-elem/course-list-elem.component';
import { CourseComponent } from './course/course.component';
import { NavbarComponent } from './navbar/navbar.component';

import { HttpClientModule } from '@angular/common/http';
import { RecommendedCourseComponent } from './recommended-course/recommended-course.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    CoursesListComponent,
    SingleCourseComponent,
    CourseListElemComponent,
    CourseComponent,
    NavbarComponent,
    RecommendedCourseComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
