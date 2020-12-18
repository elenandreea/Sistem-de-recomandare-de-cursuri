import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { CoursesListComponent } from './courses-list/courses-list.component'
import { SingleCourseComponent } from './single-course/single-course.component'

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'courses', component: CoursesListComponent},
  { path: 'course/:courseId', component: SingleCourseComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
