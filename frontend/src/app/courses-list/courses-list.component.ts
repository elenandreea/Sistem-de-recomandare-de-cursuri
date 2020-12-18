import { Component, OnInit } from '@angular/core';
import { Course } from '../course'

import { BackendConnectionService } from '../backend-connection.service';

@Component({
  selector: 'app-courses-list',
  templateUrl: './courses-list.component.html',
  styleUrls: ['./courses-list.component.css']
})
export class CoursesListComponent implements OnInit {
  courses : Course[];

  constructor(private courseService: BackendConnectionService) { }

  ngOnInit(): void {
    this.getCourses();
  }

  getCourses(): void {
    this.courseService.getCourses()
    .subscribe(courses => this.courses = courses)
  }
}
